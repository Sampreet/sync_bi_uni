#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate bidirectionally-coupled QOM systems."""

__authors__ = ['Sampreet Kalita']
__toolbox__ = 'qom-v1.0.0'
__created__ = '2020-06-03'
__updated__ = '2023-06-26'

# dependencies
import numpy as np

# qom modules
from qom.systems import BaseSystem

class Bi_00(BaseSystem):
    """Class to simulate two simple bidirectionally-coupled QOM systems.

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    system_defaults = {
        'A_l'           : 52.0,
        'Delta_0_sign'  : 1.0,
        'delta'         : 0.01,
        'g_0s'          : [0.005, 0.005],
        'gammas'        : [0.005, 0.005],
        'kappas'        : [0.15, 0.15],
        'lamb'          : 0.075,
        'n_ths'         : [0.0, 0.0],
        'omega_mL'      : 1.0
    }

    def __init__(self, params={}, cb_update=None):
        """Class constructor for Bi_00."""
        
        # initialize super class
        super().__init__(
            params=params,
            name='Bi_00',
            desc='Two Simple Bidirectionally-coupled QOM Systems',
            num_modes=4,
            cb_update=cb_update
        )

    def get_A(self, modes, c, t):
        """Method to obtain the drift matrix.

        Parameters
        ----------
        modes : numpy.ndarray
            Classical modes.
        c : numpy.ndarray, optional
            Derived constants and controls.
        t : float, optional
            Time at which the values are calculated.
        
        Returns
        -------
        A : numpy.ndarray
            Drift matrix.
        """
        
        # extract frequently used variables
        alphas  = [modes[2 * j] for j in range(2)]
        betas   = [modes[2 * j + 1] for j in range(2)]

        # effective values
        omega_ms= [self.params['omega_mL'], self.params['omega_mL'] + self.params['delta']]
        Deltas  = [self.params['Delta_0_sign'] * omega_ms[i] + 2.0 * self.params['g_0s'][i] * np.real(betas[i]) for i in range(2)]
        gs      = [self.params['g_0s'][i] * alphas[i] for i in range(2)]

        # update drift matrix
        for i in range(2):
            # X quadratures
            self.A[4*i + 0][4*i + 0] = - self.params['kappas'][i]
            self.A[4*i + 0][4*i + 1] = - Deltas[i]
            self.A[4*i + 0][4*i + 2] = - 2.0 * np.imag(gs[i])
            self.A[4*i + 0][4*(1 - i) + 1] = - self.params['lamb']
            # Y quadratures
            self.A[4*i + 1][4*i + 0] = Deltas[i]
            self.A[4*i + 1][4*i + 1] = - self.params['kappas'][i]
            self.A[4*i + 1][4*i + 2] = 2.0 * np.real(gs[i])
            self.A[4*i + 1][4*(1 - i) + 0] = self.params['lamb']
            # Q quadratures
            self.A[4*i + 2][4*i + 2] = - self.params['gammas'][i]
            self.A[4*i + 2][4*i + 3] = omega_ms[i]
            # P quadratures
            self.A[4*i + 3][4*i + 0] = 2.0 * np.real(gs[i])
            self.A[4*i + 3][4*i + 1] = 2.0 * np.imag(gs[i])
            self.A[4*i + 3][4*i + 2] = - omega_ms[i]
            self.A[4*i + 3][4*i + 3] = - self.params['gammas'][i]

        return self.A
    
    def get_D(self, modes, corrs, c, t):
        """Method to obtain the noise matrix.
        
        Parameters
        ----------
        modes : numpy.ndarray
            Classical modes.
        corrs : numpy.ndarray
            Quantum correlations.
        c : numpy.ndarray, optional
            Derived constants and controls.
        t : float, optional
            Time at which the values are calculated.
        
        Returns
        -------
        D : numpy.ndarray
            Noise matrix.
        """
        
        # update drift matrix
        for i in range(2):
            # optical modes
            self.D[4*i + 0][4*i + 0] = self.params['kappas'][i]
            self.D[4*i + 1][4*i + 1] = self.params['kappas'][i]
            # mechanical modes
            self.D[4*i + 2][4*i + 2] = self.params['gammas'][i] * (2.0 * self.params['n_ths'][i] + 1.0)
            self.D[4*i + 3][4*i + 3] = self.params['gammas'][i] * (2.0 * self.params['n_ths'][i] + 1.0)

        return self.D

    def get_ivc(self):
        """Method to obtain the initial values of the modes, correlations and derived constants and controls.
        
        Returns
        -------
        iv_modes : numpy.ndarray
            Initial values of the classical modes.
        iv_corrs : numpy.ndarray
            Initial values of the quantum correlations.
        c : numpy.ndarray
            Derived constants and controls.
        """
 
        # initial mode amplitudes
        iv_modes = np.zeros(self.num_modes, dtype=np.complex_)

        # initial quadrature correlations
        iv_corrs = np.zeros(self.dim_corrs, dtype=np.float_)
        for i in range(2):
            iv_corrs[4*i + 0][4*i + 0] = 0.5
            iv_corrs[4*i + 1][4*i + 1] = 0.5
            iv_corrs[4*i + 2][4*i + 2] = self.params['n_ths'][i] + 0.5
            iv_corrs[4*i + 3][4*i + 3] = self.params['n_ths'][i] + 0.5

        return iv_modes, iv_corrs, np.empty(0)

    def get_mode_rates(self, modes, c, t):
        """Method to obtain the rates of the classical modes.

        Parameters
        ----------
        modes : numpy.ndarray
            Classical modes.
        c : numpy.ndarray, optional
            Derived constants and controls.
        t : float, optional
            Time at which the values are calculated.
        
        Returns
        -------
        mode_rates : numpy.ndarray
            Normalized rates for each mode.
        """
        
        # extract frequently used variables
        alphas  = [modes[2 * j] for j in range(2)]
        betas   = [modes[2 * j + 1] for j in range(2)]

        # effective values
        omega_ms= [self.params['omega_mL'], self.params['omega_mL'] + self.params['delta']]
        Deltas  = [self.params['Delta_0_sign'] * omega_ms[i] + 2.0 * self.params['g_0s'][i] * np.real(betas[i]) for i in range(2)]
        gs      = [self.params['g_0s'][i] * alphas[i] for i in range(2)]

        # initialize lists
        dalpha_dts  = [(- self.params['kappas'][i] + 1.0j * Deltas[i]) * alphas[i] + 1.0j * self.params['lamb'] * alphas[1 - i] + self.params['A_l'] for i in range(2)]
        dbeta_dts   = [1.0j * gs[i] * np.conjugate(alphas[i]) + (- self.params['gammas'][i] - 1.0j * omega_ms[i]) * betas[i] for i in range(2)]

        # rearrange per system and normalize by mechanical frequency
        mode_rates = np.array([dalpha_dts[0], dbeta_dts[0], dalpha_dts[1], dbeta_dts[1]], dtype=np.complex_)

        return mode_rates