#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate unidirectionally-coupled QOM systems."""

__authors__ = ["Sampreet Kalita"]
__toolbox__ = 'qom-v1.0.1'
__created__ = "2020-01-04"
__updated__ = "2024-01-09"

# dependencies
import numpy as np

# qom modules
from qom.systems import BaseSystem

class Uni_00(BaseSystem):
    r"""Class to simulate a two simple unidirectionally-coupled QOM systems.

    Parameters
    ----------
    params : dict
        Parameters for the system. The system parameters are:
        ============    ====================================================================
        key             meaning
        ============    ====================================================================
        A_l             (*float*) amplitude of the laser :math:`A_{l}`. Default is :math:`52.0`.
        Delta_0_sign    (*float*) sign of the laser detuning. Default is :math:`1.0`.
        delta           (*float*) normalized detuning of the right mechanical mode from the left, :math:`\delta = \omega_{mR} / \omega_{mL} - 1`. Default is :math:`0.01`.
        eta             (*float*) transmission coefficient of the optical channel :math:`\eta`. Default is :math:`0.75`.
        g_0s            (*list*) normalized optomechanical coupling strengths, in the format :math:`\left[ g_{0L}, g_{0R} \right]`. Default is :math:`\left[ 0.005, 0.005 \right]`.
        gammas          (*list*) normalized mechanical decay rates, in the format :math:`\left[ \gamma_{L}, \gamma_{R} \right]`. Default is :math:`\left[ 0.005, 0.005 \right]`.
        kappas          (*list*) normalized optical decay rates, in the format :math:`\left[ \kappa_{L}, \kappa_{R} \right]`. Default is :math:`\left[ 0.15, 0.15 \right]`.
        n_ths           (*list*) thermal occupancies of the mechanical modes, :math:`\left[ n_{thL}, n_{thR} \right]`. Default is :math:`\left[ 0.005, 0.005 \right]`.
        omega_mL        (*float*) normalized frequency of the left mechanical mode :math:`\omega_{mL}`. Default is :math:`1.0`.
        ============    ====================================================================
    cb_update : callable, optional
        Callback function to update status and progress, formatted as ``cb_update(status, progress, reset)``, where ``status`` is a string, ``progress`` is a float and ``reset`` is a boolean.
    """

    system_defaults = {
        'A_l'           : 52.0,
        'Delta_0_sign'  : 1.0,
        'delta'         : 0.01,
        'eta'           : 0.75,
        'g_0s'          : [0.005, 0.005],
        'gammas'        : [0.005, 0.005],
        'kappas'        : [0.15, 0.15],
        'n_ths'         : [0.0, 0.0],
        'omega_mL'      : 1.0
    }

    def __init__(self, params, cb_update=None):
        """Class constructor for Uni_00."""
        
        # initialize super class
        super().__init__(
            params=params,
            name='Uni_00',
            desc='Two Simple Unidirectionally-coupled QOM Systems',
            num_modes=4,
            cb_update=cb_update
        )

    def get_A(self, modes, c, t):
        """Method to obtain the drift matrix.

        Parameters
        ----------
        modes : numpy.ndarray
            Classical modes.
        c : numpy.ndarray
            Derived constants and controls.
        t : float
            Time at which the values are calculated.
        
        Returns
        -------
        A : numpy.ndarray
            Drift matrix.
        """
        
        # extract frequently used variables
        alphas = [modes[2 * j] for j in range(2)]
        betas = [modes[2 * j + 1] for j in range(2)]
        temp = np.sqrt(self.params['eta'] * self.params['kappas'][0] * self.params['kappas'][1])

        # effective values
        omega_ms= [self.params['omega_mL'], self.params['omega_mL'] + self.params['delta']]
        Deltas = [self.params['Delta_0_sign'] * omega_ms[i] + 2.0 * self.params['g_0s'][i] * np.real(betas[i]) for i in range(2)]
        gs = [self.params['g_0s'][i] * alphas[i] for i in range(2)]

        # udpate drift matrix
        for i in range(2):
            # X quadratures
            self.A[4*i + 0][4*i + 0] = - self.params['kappas'][i]
            self.A[4*i + 0][4*i + 1] = - Deltas[i]
            self.A[4*i + 0][4*i + 2] = - 2.0 * np.imag(gs[i])
            # Y quadratures
            self.A[4*i + 1][4*i + 0] = Deltas[i]
            self.A[4*i + 1][4*i + 1] = - self.params['kappas'][i]
            self.A[4*i + 1][4*i + 2] = 2.0 * np.real(gs[i])
            # Q quadratures
            self.A[4*i + 2][4*i + 2] = - self.params['gammas'][i]
            self.A[4*i + 2][4*i + 3] = omega_ms[i]
            # P quadratures
            self.A[4*i + 3][4*i + 0] = 2.0 * np.real(gs[i])
            self.A[4*i + 3][4*i + 1] = 2.0 * np.imag(gs[i])
            self.A[4*i + 3][4*i + 2] = - omega_ms[i]
            self.A[4*i + 3][4*i + 3] = - self.params['gammas'][i]
        self.A[4][0] = - 2 * temp
        self.A[5][1] = - 2 * temp

        return self.A
    
    def get_D(self, modes, corrs, c, t):
        """Method to obtain the noise matrix.
        
        Parameters
        ----------
        modes : numpy.ndarray
            Classical modes.
        corrs : numpy.ndarray
            Quantum correlations.
        c : numpy.ndarray
            Derived constants and controls.
        t : float
            Time at which the values are calculated.
        
        Returns
        -------
        D : numpy.ndarray
            Noise matrix.
        """
        
        # extract frequently used variables
        temp = np.sqrt(self.params['eta'] * self.params['kappas'][0] * self.params['kappas'][1])
        
        # update drift matrix
        for i in range(2):
            # optical modes
            self.D[4*i + 0][4*i + 0] = self.params['kappas'][i]
            self.D[4*i + 1][4*i + 1] = self.params['kappas'][i]
            # mechanical modes
            self.D[4*i + 2][4*i + 2] = self.params['gammas'][i] * (2.0 * self.params['n_ths'][i] + 1)
            self.D[4*i + 3][4*i + 3] = self.params['gammas'][i] * (2.0 * self.params['n_ths'][i] + 1)
        self.D[0][4] = temp
        self.D[1][5] = temp
        self.D[4][0] = temp
        self.D[5][1] = temp

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
        """Method to obtain the rates of change of the modes.

        Parameters
        ----------
        modes : numpy.ndarray
            Classical modes.
        c : numpy.ndarray
            Derived constants and controls.
        t : float
            Time at which the values are calculated.
        
        Returns
        -------
        mode_rates : numpy.ndarray
            Rates of change of the modes.
        """

        # extract frequently used variables
        alphas = modes[::2]
        betas = modes[1::2]

        # effective values
        omega_ms= [
            self.params['omega_mL'],
            self.params['omega_mL'] + self.params['delta']
        ]
        Deltas = [self.params['Delta_0_sign'] * omega_ms[i] + 2.0 * self.params['g_0s'][i] * np.real(betas[i]) for i in range(2)]
        gs = [self.params['g_0s'][i] * alphas[i] for i in range(2)]

        # optical modes
        dalpha_dts = [(- self.params['kappas'][i] + 1.0j * Deltas[i]) * alphas[i] for i in range(2)]
        dalpha_dts[0] += self.params['A_l']
        dalpha_dts[1] += - 2.0 * np.sqrt(self.params['eta'] * self.params['kappas'][0] * self.params['kappas'][1]) * alphas[0] + (np.sqrt(self.params['eta']) + np.sqrt(1.0 - self.params['eta'])) * self.params['A_l']
        # mechanical modes
        dbeta_dts = [1.0j * gs[i] * np.conjugate(alphas[i]) + (- self.params['gammas'][i] - 1.0j * omega_ms[i]) * betas[i] for i in range(2)]
        
        return np.array([dalpha_dts[0], dbeta_dts[0], dalpha_dts[1], dbeta_dts[1]], dtype=np.complex_)

class Uni_01(BaseSystem):
    """Class to simulate two simple unidirectionally-coupled QOM systems with Plus-Minus modes.

    Parameters
    ----------
    params : dict
        Parameters for the system. The system parameters are:
        ============    ====================================================================
        key             meaning
        ============    ====================================================================
        A_l             (*float*) amplitude of the laser :math:`A_{l}`. Default is :math:`52.0`.
        Delta_0_sign    (*float*) sign of the laser detuning. Default is :math:`1.0`.
        delta           (*float*) normalized detuning of the right mechanical mode from the left, :math:`\delta = \omega_{mR} / \omega_{mL} - 1`. Default is :math:`0.01`.
        eta             (*float*) transmission coefficient of the optical channel :math:`\eta`. Default is :math:`0.75`.
        g_0s            (*list*) normalized optomechanical coupling strengths, in the format :math:`\left[ g_{0L}, g_{0R} \right]`. Default is :math:`\left[ 0.005, 0.005 \right]`.
        gammas          (*list*) normalized mechanical decay rates, in the format :math:`\left[ \gamma_{L}, \gamma_{R} \right]`. Default is :math:`\left[ 0.005, 0.005 \right]`.
        kappas          (*list*) normalized optical decay rates, in the format :math:`\left[ \kappa_{L}, \kappa_{R} \right]`. Default is :math:`\left[ 0.15, 0.15 \right]`.
        n_ths           (*list*) thermal occupancies of the mechanical modes, :math:`\left[ n_{thL}, n_{thR} \right]`. Default is :math:`\left[ 0.005, 0.005 \right]`.
        omega_mL        (*float*) normalized frequency of the left mechanical mode :math:`\omega_{mL}`. Default is :math:`1.0`.
        ============    ====================================================================
    cb_update : callable, optional
        Callback function to update status and progress, formatted as ``cb_update(status, progress, reset)``, where ``status`` is a string, ``progress`` is a float and ``reset`` is a boolean.
    """

    system_defaults = {
        'A_l'           : 52.0,
        'Delta_0_sign'  : 1.0,
        'delta'         : 0.01,
        'eta'           : 0.75,
        'g_0s'          : [0.005, 0.005],
        'gammas'        : [0.005, 0.005],
        'kappas'        : [0.15, 0.15],
        'n_ths'         : [0.0, 0.0],
        'omega_mL'      : 1.0
    }

    def __init__(self, params, cb_update=None):
        """Class constructor for Uni_01."""
        
        # initialize super class
        super().__init__(
            params=params,
            name='Uni_01',
            desc='Two Simple Unidirectionally-coupled QOM Systems with Plus-Minus modes',
            num_modes=4,
            cb_update=cb_update
        )

    def get_A(self, modes, c, t):
        """Method to obtain the drift matrix.

        Parameters
        ----------
        modes : numpy.ndarray
            Classical modes.
        c : numpy.ndarray
            Derived constants and controls.
        t : float
            Time at which the values are calculated.
        
        Returns
        -------
        A : numpy.ndarray
            Drift matrix.
        """
        
        # extract frequently used variables
        alphas = modes[::2]
        betas = modes[1::2]
        temp = np.sqrt(self.params['eta'] * self.params['kappas'][0] * self.params['kappas'][1])

        # effective values
        omega_ms= [self.params['omega_mL'], self.params['omega_mL'] + self.params['delta']]
        Deltas = [self.params['Delta_0_sign'] * omega_ms[i] + 2.0 * self.params['g_0s'][i] * np.real(betas[i]) for i in range(2)]
        gs = [self.params['g_0s'][i] * alphas[i] for i in range(2)]

        # update drift matrix
        for i in range(2):
            # sign of mode
            _sign = - 2.0 * (i - 0.5)
            # X quadratures
            self.A[4*i + 0][0] = - self.params['kappas'][0] / 2.0 - _sign * self.params['kappas'][1] / 2.0 - _sign * temp
            self.A[4*i + 0][1] = - Deltas[0] / 2.0 - _sign * Deltas[1] / 2.0
            self.A[4*i + 0][2] = - np.imag(gs[0]) - _sign * np.imag(gs[1])
            self.A[4*i + 0][4] = - self.params['kappas'][0] / 2.0 + _sign * self.params['kappas'][1] / 2.0 - _sign * temp
            self.A[4*i + 0][5] = - Deltas[0] / 2.0 + _sign * Deltas[1] / 2.0
            self.A[4*i + 0][6] = - np.imag(gs[0]) + _sign * np.imag(gs[1])
            # Y quadratures
            self.A[4*i + 1][0] = Deltas[0] / 2.0 + _sign * Deltas[1] / 2.0
            self.A[4*i + 1][1] = - self.params['kappas'][0] / 2.0 - _sign * self.params['kappas'][1] / 2.0 - _sign * temp
            self.A[4*i + 1][2] = np.real(gs[0]) + _sign * np.real(gs[1])
            self.A[4*i + 1][4] = Deltas[0] / 2.0 - _sign * Deltas[1] / 2.0
            self.A[4*i + 1][5] = - self.params['kappas'][0] / 2.0 + _sign * self.params['kappas'][1] / 2.0 - _sign * temp
            self.A[4*i + 1][6] = np.real(gs[0]) - _sign * np.real(gs[1])
            # Q quadratures
            self.A[4*i + 2][2] = - self.params['gammas'][0] / 2.0 - _sign * self.params['gammas'][1] / 2.0
            self.A[4*i + 2][3] = omega_ms[0] / 2.0 + _sign * omega_ms[1] / 2.0
            self.A[4*i + 2][6] = - self.params['gammas'][0] / 2.0 + _sign * self.params['gammas'][1] / 2.0
            self.A[4*i + 2][7] = omega_ms[0] / 2.0 - _sign * omega_ms[1] / 2.0
            # P quadratures
            self.A[4*i + 3][0] = np.real(gs[0]) + _sign * np.real(gs[1])
            self.A[4*i + 3][1] = np.imag(gs[0]) + _sign * np.imag(gs[1])
            self.A[4*i + 3][2] = - omega_ms[0] / 2.0 - _sign * omega_ms[1] / 2.0
            self.A[4*i + 3][3] = - self.params['gammas'][0] / 2.0 - _sign * self.params['gammas'][1] / 2.0
            self.A[4*i + 3][4] = np.real(gs[0]) - _sign * np.real(gs[1])
            self.A[4*i + 3][5] = np.imag(gs[0]) - _sign * np.imag(gs[1])
            self.A[4*i + 3][6] = - omega_ms[0] / 2.0 + _sign * omega_ms[1] / 2.0
            self.A[4*i + 3][7] = - self.params['gammas'][0] / 2.0 + _sign * self.params['gammas'][1] / 2.0

        return self.A
    
    def get_D(self, modes, corrs, c, t):
        """Method to obtain the noise matrix.
        
        Parameters
        ----------
        modes : numpy.ndarray
            Classical modes.
        corrs : numpy.ndarray
            Quantum correlations.
        c : numpy.ndarray
            Derived constants and controls.
        t : float
            Time at which the values are calculated.
        
        Returns
        -------
        D : numpy.ndarray
            Noise matrix.
        """
        
        # extract frequently used variables
        temp = np.sqrt(self.params['eta'] * self.params['kappas'][0] * self.params['kappas'][1])

        # update drift matrix
        for i in range(2):
            # sign of mode
            _sign = - 2 * (i - 0.5)
            # alternate index 
            _ai = 1 if i == 0 else 0
            # X
            self.D[4*i + 0][4*i + 0] = self.params['kappas'][0] / 2.0 + self.params['kappas'][1] / 2.0 + _sign * temp
            self.D[4*i + 0][4*_ai + 0] = self.params['kappas'][0] / 2.0 - self.params['kappas'][1] / 2.0
            # Y
            self.D[4*i + 1][4*i + 1] = self.params['kappas'][0] / 2.0 + self.params['kappas'][1] / 2.0 + _sign * temp
            self.D[4*i + 1][4*_ai + 1] = self.params['kappas'][0] / 2.0 - self.params['kappas'][1] / 2.0
            # Q
            self.D[4*i + 2][4*i + 2] = self.params['gammas'][0] * (self.params['n_ths'][0] + 0.5) + self.params['gammas'][1] * (self.params['n_ths'][1] + 0.5)
            self.D[4*i + 2][4*_ai + 2] = self.params['gammas'][0] * (self.params['n_ths'][0] + 0.5) + self.params['gammas'][1] * (self.params['n_ths'][1] + 0.5)
            # P
            self.D[4*i + 3][4*i + 3] = self.params['gammas'][0] * (self.params['n_ths'][0] + 0.5) + self.params['gammas'][1] * (self.params['n_ths'][1] + 0.5)
            self.D[4*i + 3][4*_ai + 3] = self.params['gammas'][0] * (self.params['n_ths'][0] + 0.5) + self.params['gammas'][1] * (self.params['n_ths'][1] + 0.5)

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
            # alternate index 
            _ai = 1 if i == 0 else 0
            iv_corrs[4*i + 0][4*i + 0] = 0.5
            iv_corrs[4*i + 0][4*_ai + 0] = 0.5
            iv_corrs[4*i + 1][4*i + 1] = 0.5
            iv_corrs[4*i + 1][4*_ai + 1] = 0.5
            iv_corrs[4*i + 2][4*i + 2] = self.params['n_ths'][i] + 0.5
            iv_corrs[4*i + 2][4*_ai + 2] = self.params['n_ths'][i] + 0.5
            iv_corrs[4*i + 3][4*i + 3] = self.params['n_ths'][i] + 0.5
            iv_corrs[4*i + 3][4*_ai + 3] = self.params['n_ths'][i] + 0.5

        return iv_modes, iv_corrs, np.empty(0)

    def get_mode_rates(self, modes, c, t):
        """Method to obtain the rates of change of the modes.

        Parameters
        ----------
        modes : numpy.ndarray
            Classical modes.
        c : numpy.ndarray
            Derived constants and controls.
        t : float
            Time at which the values are calculated.
        
        Returns
        -------
        mode_rates : numpy.ndarray
            Rates of change of the modes.
        """

        # extract frequently used variables
        alphas = modes[::2]
        betas = modes[1::2]

        # effective values
        omega_ms = [
            self.params['omega_mL'],
            self.params['omega_mL'] + self.params['delta']
        ]
        Deltas = [self.params['Delta_0_sign'] * omega_ms[i] + 2.0 * self.params['g_0s'][i] * np.real(betas[i]) for i in range(2)]
        gs = [self.params['g_0s'][i] * alphas[i] for i in range(2)]

        # optical modes
        dalpha_dts = [(- self.params['kappas'][i] + 1.0j * Deltas[i]) * alphas[i] for i in range(2)]
        dalpha_dts[0] += self.params['A_l']
        dalpha_dts[1] += - 2.0 * np.sqrt(self.params['eta'] * self.params['kappas'][0] * self.params['kappas'][1]) * alphas[0] + (np.sqrt(self.params['eta']) + np.sqrt(1.0 - self.params['eta'])) * self.params['A_l']
        # mechanical modes
        dbeta_dts = [1.0j * gs[i] * np.conjugate(alphas[i]) + (- self.params['gammas'][i] - 1.0j * omega_ms[i]) * betas[i] for i in range(2)]
        
        return np.array([dalpha_dts[0], dbeta_dts[0], dalpha_dts[1], dbeta_dts[1]], dtype=np.complex_)