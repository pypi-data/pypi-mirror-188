'''
Notices:
Copyright 2018 United States Government as represented by the Administrator of
the National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S. Code. All Other Rights Reserved.

Disclaimers
No Warranty: THE SUBJECT SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTY OF
ANY KIND, EITHER EXPRessED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED
TO, ANY WARRANTY THAT THE SUBJECT SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY
IMPLIED WARRANTIES OF MERCHANTABILITY, FITNess FOR A PARTICULAR PURPOSE, OR
FREEDOM FROM INFRINGEMENT, ANY WARRANTY THAT THE SUBJECT SOFTWARE WILL BE ERROR
FREE, OR ANY WARRANTY THAT DOCUMENTATION, IF PROVIDED, WILL CONFORM TO THE
SUBJECT SOFTWARE. THIS AGREEMENT DOES NOT, IN ANY MANNER, CONSTITUTE AN
ENDORSEMENT BY GOVERNMENT AGENCY OR ANY PRIOR RECIPIENT OF ANY RESULTS,
RESULTING DESIGNS, HARDWARE, SOFTWARE PRODUCTS OR ANY OTHER APPLICATIONS
RESULTING FROM USE OF THE SUBJECT SOFTWARE.  FURTHER, GOVERNMENT AGENCY
DISCLAIMS ALL WARRANTIES AND LIABILITIES REGARDING THIRD-PARTY SOFTWARE, IF
PRESENT IN THE ORIGINAL SOFTWARE, AND DISTRIBUTES IT "AS IS."

Waiver and Indemnity:  RECIPIENT AGREES TO WAIVE ANY AND ALL CLAIMS AGAINST THE
UNITED STATES GOVERNMENT, ITS CONTRACTORS AND SUBCONTRACTORS, AS WELL AS ANY
PRIOR RECIPIENT.  IF RECIPIENT'S USE OF THE SUBJECT SOFTWARE RESULTS IN ANY
LIABILITIES, DEMANDS, DAMAGES, EXPENSES OR LOSSES ARISING FROM SUCH USE,
INCLUDING ANY DAMAGES FROM PRODUCTS BASED ON, OR RESULTING FROM, RECIPIENT'S
USE OF THE SUBJECT SOFTWARE, RECIPIENT SHALL INDEMNIFY AND HOLD HARMLess THE
UNITED STATES GOVERNMENT, ITS CONTRACTORS AND SUBCONTRACTORS, AS WELL AS ANY
PRIOR RECIPIENT, TO THE EXTENT PERMITTED BY LAW.  RECIPIENT'S SOLE REMEDY FOR
ANY SUCH MATTER SHALL BE THE IMMEDIATE, UNILATERAL TERMINATION OF THIS
AGREEMENT.
'''

import numpy as np

from scipy.optimize import bisect
from tqdm import tqdm

from .sampler_base import SamplerBase
from .smc.updater import Updater
from .utils.progress_bar import set_bar
from .utils.mpi_utils import rank_zero_output_only


class FixedSampler(SamplerBase):
    '''
    SMC sampler using a fixed phi sequence.
    '''
    def __init__(self, mcmc_kernel):
        '''
        :param mcmc_kernel: a kernel object for conducting particle mutation
        :type mcmc_kernel: MCMCKernel object
        '''
        super().__init__(mcmc_kernel)

    def sample(self,
               num_particles,
               num_mcmc_samples,
               phi_sequence,
               ess_threshold,
               proposal=None,
               progress_bar=True):
        '''
        :param num_particles: number of particles
        :type num_particles: int
        :param num_mcmc_samples: number of MCMC samples to draw from the
            MCMC kernel per iteration per particle
        :type num_mcmc_samples: int
        :param phi_sequence: increasing monotonic sequence of floats starting
            at 0 and ending at 1; sometimes referred to as tempering schedule
        :type phi_sequence: list or array
        :param ess_threshold: the effective sample size at which resampling
            should be conducted; given as a fraction of num_particles and must
            be in the range [0, 1]
        :type ess_threshold: float
        :param proposal: tuple of samples from a proposal distribution used to
            initialize the SMC sampler; first element is a dictionary with keys
            equal to parameter names and values equal to corresponding samples;
            second element is array of corresponding proposal PDF values
        :type proposal: tuple(dict, array)
        :param progress_bar: display progress bar during sampling
        :type progress_bar: bool
        '''
        self._updater = Updater(ess_threshold)
        self._phi_sequence = phi_sequence

        self.step = self._initialize(num_particles, proposal)

        phi_iterator = self._phi_sequence[1:]
        if progress_bar:
            phi_iterator = tqdm(phi_iterator)
        set_bar(phi_iterator, 1, self._mutation_ratio, self._updater)

        for i, phi in enumerate(phi_iterator):
            dphi = phi - self._phi_sequence[i]
            self._do_smc_step(phi, dphi, num_mcmc_samples)
            set_bar(phi_iterator, i + 2, self._mutation_ratio, self._updater)

        return self._result, self._result.estimate_marginal_log_likelihoods()


class AdaptiveSampler(SamplerBase):
    '''
    SMC sampler using an adaptive phi sequence.
    '''
    def __init__(self, mcmc_kernel):
        '''
        :param mcmc_kernel: a kernel object for conducting particle mutation
        :type mcmc_kernel: MCMCKernel object
        '''
        self.req_phi_index = None
        super().__init__(mcmc_kernel)

    def sample(self,
               num_particles,
               num_mcmc_samples,
               target_ess=0.8,
               proposal=None,
               required_phi=1,
               progress_bar=True):
        '''
        :param num_particles: number of particles
        :type num_particles: int
        :param num_mcmc_samples: number of MCMC samples to draw from the
            MCMC kernel per iteration per particle
        :type num_mcmc_samples: int
        :param target_ess: controls adaptive stepping by picking the next
            phi such that the effective sample size is equal to the threshold.
            Specified as a fraction of total number particles (between 0 and 1).
        :type target_ess: float
        :param proposal: tuple of samples from a proposal distribution used to
            initialize the SMC sampler; first element is a dictionary with keys
            equal to parameter names and values equal to corresponding samples;
            second element is array of corresponding proposal PDF values
        :type proposal: tuple(dict, array)
        :param required_phi: specific values of phi that must be included in
            the phi sequence (regardless of optimized step)
        :type required_phi: float, int, or list
        '''
        self._updater = Updater(ess_threshold=1)  # ensure always resampling
        self._phi_sequence = [0]

        self.step = self._initialize(num_particles, proposal)

        pbar = self._init_progress_bar(progress_bar)

        while self._phi_sequence[-1] < 1:
            phi = self.optimize_step(self.step, self._phi_sequence[-1],
                                     target_ess, required_phi)
            dphi = phi - self._phi_sequence[-1]
            self._do_smc_step(phi, dphi, num_mcmc_samples)
            self._phi_sequence.append(phi)
            self._update_progress_bar(pbar, dphi)

        self._close_progress_bar(pbar)

        self.req_phi_index = [i for i, phi in enumerate(self.phi_sequence) \
                              if phi in self._as_phi_list(required_phi)]

        return self._result, self._result.estimate_marginal_log_likelihoods()

    @rank_zero_output_only
    def optimize_step(self, particles, phi_old, target_ess=1, required_phi=1):
        phi = 1
        if not self._full_step_meets_target(phi_old, particles, target_ess):
            phi = bisect(self.predict_ess_margin,
                         phi_old,
                         1,
                         args=(phi_old, particles, target_ess))
        proposed_phi_list = self._as_phi_list(required_phi)
        proposed_phi_list.append(phi)
        return self._select_phi(proposed_phi_list, phi_old)

    def predict_ess_margin(self, phi_new, phi_old, particles, target_ess=1):
        delta_phi = phi_new - phi_old
        beta = np.exp((delta_phi) * particles.log_likes) if delta_phi > 0 \
               else np.ones_like(particles.log_likes)
        numer = np.sum(beta)**2
        denom = np.sum(beta**2)
        ESS = 0
        if numer > 0 and denom > 0:
            ESS = numer / denom
        return ESS - particles.num_particles * target_ess

    @staticmethod
    def _as_phi_list(phi):
        if not isinstance(phi, list):
            phi = [phi]
        phi = sorted([p for p in phi if p < 1])
        return phi

    @staticmethod
    def _select_phi(proposed_phi_list, phi_old):
        return min([p for p in proposed_phi_list if p > phi_old])

    def _full_step_meets_target(self, phi_old, particles, target_ess):
        return self.predict_ess_margin(1, phi_old, particles, target_ess) > 0

    def _init_progress_bar(self, progress_bar):
        pbar = False
        if progress_bar:
            bar_format =  "{desc}: {percentage:.2f}%|{bar}| " + \
                       "phi: {n:.5f}/{total_fmt} [{elapsed}<{remaining}"
            pbar = tqdm(total=1.0, bar_format=bar_format)
            pbar.set_description('[ mutation ratio: n/a')
            pbar.update(0)
        return pbar

    def _update_progress_bar(self, pbar, dphi):
        if pbar:
            pbar.set_description(f'[ mutation ratio: {self._mutation_ratio}')
            pbar.update(dphi)

    @staticmethod
    def _close_progress_bar(pbar):
        if pbar:
            pbar.close()
