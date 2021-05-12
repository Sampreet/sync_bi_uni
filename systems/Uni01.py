#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate a unidirectionally-coupled configuration of QOM systems with Plus-Minus modes."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-01-28'
__updated__ = '2021-05-12'

# dependencies
import numpy as np

# qom modules
from qom.systems import DODMSystem

class Uni01(DODMSystem):
    """Class to simulate a simple unidirectionally-coupled configuration of QOM systems with Plus-Minus modes.

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for Uni01."""
        
        # initialize super class
        super().__init__(params)

        # update code and name
        self.code = 'uni_01'
        self.name = 'Unidirectional QOM System with Plus-Minus Modes'
        
        # default parameters
        self.params = {
            'A_l': params.get('A_l', 70.0),
            'Delta_0': params.get('Delta_0', 1.0),
            'delta': params.get('delta', 0.005),
            'eta': params.get('eta', 0.75),
            'g_0s': params.get('g_0s', [0.005, 0.005]),
            'gammas': params.get('gammas', [0.005, 0.005]),
            'kappas': params.get('kappas', [0.15, 0.15]),
            'n_ths': params.get('n_ths', [0, 0]),
            'omega_m': params.get('omega_m', 1.0),
        }
        # matrices
        self.A = None
        self.D = None

    def get_A(self, modes):
        """Function to obtain the drift matrix.

        Parameters
        ----------
        modes : list
            Values of the optical and mechancial modes.
        
        Returns
        -------
        A : list
            Drift matrix.
        """

        # extract frequently used variables
        eta     = self.params['eta']
        g_0s    = self.params['g_0s']
        gammas  = self.params['gammas']
        kappas  = self.params['kappas']
        temp = np.sqrt(eta * kappas[0] * kappas[1])
        alphas  = [modes[0], modes[2]]
        betas   = [modes[1], modes[3]]

        # get frequencies
        omega_ms, Delta_0s = self.get_frequencies()

        # effective detunings
        Deltas  = list()
        gs      = list()
        for i in range(2):
            Deltas.append(Delta_0s[i] + 2 * g_0s[i] * np.real(betas[i]))
            gs.append(g_0s[i] * alphas[i])

        # drift matrix
        if self.A is None or np.shape(self.A) != (8, 8):
            self.A = np.zeros([8, 8], dtype=np.float_)
        for i in range(2):
            # sign of mode
            _sign = - 2 * (i - 0.5)
            # X
            self.A[4*i + 0][0] = - kappas[0] / 2 - _sign * kappas[1] / 2 - _sign * temp
            self.A[4*i + 0][1] = - Deltas[0] / 2 - _sign * Deltas[1] / 2
            self.A[4*i + 0][2] = - np.imag(gs[0]) - _sign * np.imag(gs[1])
            self.A[4*i + 0][4] = - kappas[0] / 2 + _sign * kappas[1] / 2 - _sign * temp
            self.A[4*i + 0][5] = - Deltas[0] / 2 + _sign * Deltas[1] / 2
            self.A[4*i + 0][6] = - np.imag(gs[0]) + _sign * np.imag(gs[1])
            # Y
            self.A[4*i + 1][0] = Deltas[0] / 2 + _sign * Deltas[1] / 2
            self.A[4*i + 1][1] = - kappas[0] / 2 - _sign * kappas[1] / 2 - _sign * temp
            self.A[4*i + 1][2] = np.real(gs[0]) + _sign * np.real(gs[1])
            self.A[4*i + 1][4] = Deltas[0] / 2 - _sign * Deltas[1] / 2
            self.A[4*i + 1][5] = - kappas[0] / 2 + _sign * kappas[1] / 2 - _sign * temp
            self.A[4*i + 1][6] = np.real(gs[0]) - _sign * np.real(gs[1])
            # Q
            self.A[4*i + 2][2] = - gammas[0] / 2 - _sign * gammas[1] / 2
            self.A[4*i + 2][3] = omega_ms[0] / 2 + _sign * omega_ms[1] / 2
            self.A[4*i + 2][6] = - gammas[0] / 2 + _sign * gammas[1] / 2
            self.A[4*i + 2][7] = omega_ms[0] / 2 - _sign * omega_ms[1] / 2
            # P
            self.A[4*i + 3][0] = np.real(gs[0]) + _sign * np.real(gs[1])
            self.A[4*i + 3][1] = np.imag(gs[0]) + _sign * np.imag(gs[1])
            self.A[4*i + 3][2] = - omega_ms[0] / 2 - _sign * omega_ms[1] / 2
            self.A[4*i + 3][3] = - gammas[0] / 2 - _sign * gammas[1] / 2
            self.A[4*i + 3][4] = np.real(gs[0]) - _sign * np.real(gs[1])
            self.A[4*i + 3][5] = np.imag(gs[0]) - _sign * np.imag(gs[1])
            self.A[4*i + 3][6] = - omega_ms[0] / 2 + _sign * omega_ms[1] / 2
            self.A[4*i + 3][7] = - gammas[0] / 2 + _sign * gammas[1] / 2

        return self.A

    def get_D(self):
        """Function to obtain the noise correlation matrix.
        
        Returns
        -------
        D : list
            Noise correlation matrix.
        """

        # extract frequently used variables
        eta     = self.params['eta']
        gammas  = self.params['gammas']
        kappas  = self.params['kappas']
        n_ths   = self.params['n_ths']
        temp    = np.sqrt(eta * kappas[0] * kappas[1])

        # noise correlation matrix
        if self.D is None or np.shape(self.D) != (8, 8):
            self.D = np.zeros([8, 8], dtype=np.float_)
        for i in range(2):
            # sign of mode
            _sign = - 2 * (i - 0.5)
            # alternate index 
            _ai = 1 if i == 0 else 0
            # X
            self.D[4*i + 0][4*i + 0] = kappas[0] / 2 + kappas[1] / 2 + _sign * temp
            self.D[4*i + 0][4*_ai + 0] = kappas[0] / 2 - kappas[1] / 2
            # Y
            self.D[4*i + 1][4*i + 1] = kappas[0] / 2 + kappas[1] / 2 + _sign * temp
            self.D[4*i + 1][4*_ai + 1] = kappas[0] / 2 - kappas[1] / 2
            # Q
            self.D[4*i + 2][4*i + 2] = gammas[0] * (n_ths[0] + 1 / 2) + gammas[1] * (n_ths[1] + 1 / 2)
            self.D[4*i + 2][4*_ai + 2] = gammas[0] * (n_ths[0] + 1 / 2) + gammas[1] * (n_ths[1] + 1 / 2)
            # P
            self.D[4*i + 3][4*i + 3] = gammas[0] * (n_ths[0] + 1 / 2) + gammas[1] * (n_ths[1] + 1 / 2)
            self.D[4*i + 3][4*_ai + 3] = gammas[0] * (n_ths[0] + 1 / 2) + gammas[1] * (n_ths[1] + 1 / 2)

        return self.D

    def get_frequencies(self):
        """Function to obtain the mechanical frequencies and laser detunings.
        
        Returns
        -------
        omega_ms : list
            Mechanical frequencies.
        Delta_0s : list
            Laser detunings.
        """
        
        # extract frequently used variables
        delta       = self.params['delta']
        Delta_0     = self.params['Delta_0']
        omega_m     = self.params['omega_m']

        # mechanical frequencies
        omega_ms = [omega_m, omega_m + delta]
        # laser detunings
        Delta_0s = omega_ms
        if Delta_0 < 0:
            Delta_0s = - 1 * omega_ms
            
        return omega_ms, Delta_0s

    def get_rates_modes(self, values):
        """Function to obtain the rates of the optical and mechanical modes.
        
        Parameters
        ----------
        values : list
            Values of the modes.
        
        Returns
        -------
        mode_rates : list
            Rates for each mode.
        """
        
        # extract frequently used variables
        A_l     = self.params['A_l']
        eta     = self.params['eta']
        g_0s    = self.params['g_0s']
        gammas  = self.params['gammas']
        kappas  = self.params['kappas']
        alphas  = [values[0], values[2]]
        betas   = [values[1], values[3]]

        # get frequencies
        Delta_0s, omega_ms = self.get_frequencies()

        # initialize lists
        Deltas      = list()
        gs          = list()
        dalpha_dts  = list()
        dbeta_dts   = list()

        # effective detunings
        for i in range(2):
            Deltas.append(Delta_0s[i] + 2 * g_0s[i] * np.real(betas[i]))
            gs.append(g_0s[i] * alphas[i])

        # calculate rates
        for i in range(2):
            dalpha_dts.append((-kappas[i] + 1j * Deltas[i]) * alphas[i])
            dbeta_dts.append(1j * gs[i] * np.conjugate(alphas[i]) + (-gammas[i] - 1j * omega_ms[i]) * betas[i])
        dalpha_dts[0] += A_l
        dalpha_dts[1] += - 2 * np.sqrt(eta * kappas[0] * kappas[1]) * alphas[0] + (np.sqrt(eta) + np.sqrt(1 - eta)) * A_l
        
        # rearrange per system
        mode_rates = [dalpha_dts[0], dbeta_dts[0], dalpha_dts[1], dbeta_dts[1]]

        return mode_rates

    def ivc_func(self):
        """Function to obtain the initial values and constants required for the IVP.
        
        Returns
        -------
        iv : list
            Initial values of variables.

        c : list
            Constant parameters.
        """

        # extract frequently used variables
        # mechanical mode frequency
        n_ths    = self.params['n_ths']
 
        # initial mode values as 1D list
        u_0 = np.zeros(4, dtype=np.complex_).tolist()

        # initial quadrature correlations
        V_0 = np.zeros([8, 8], dtype=np.float_)
        for i in range(2):
            # alternate index 
            _ai = 1 if i == 0 else 0
            V_0[4*i + 0][4*i + 0] = 1 / 2
            V_0[4*i + 0][4*_ai + 0] = 1 / 2
            V_0[4*i + 1][4*i + 1] = 1 / 2
            V_0[4*i + 1][4*_ai + 1] = 1 / 2
            V_0[4*i + 2][4*i + 2] = (n_ths[i] + 1 / 2)
            V_0[4*i + 2][4*_ai + 2] = (n_ths[i] + 1 / 2)
            V_0[4*i + 3][4*i + 3] = (n_ths[i] + 1 / 2)
            V_0[4*i + 3][4*_ai + 3] = (n_ths[i] + 1 / 2)

        # convert to 1D list and concatenate all variables
        v = u_0 + [np.complex_(element) for element in V_0.flatten()]

        # return concatenated lists of variables and constants
        return v, None

    def ode_func(self, t, v):
        """Model function for the rate equations of the modes and correlations.
        
        The variables are complex-valued, hence the model requires a complex-valued integrator.
        
        Parameters
        ----------
        t : *float*
            Time at which the rate is calculated.

        v : list
            Complex-valued variables defining the system. 
            First 2 elements contain the optical and mechanical modes of the 1st cavity.
            Next 2 elements contain the optical and mechanical modes of the 2nd cavity.
            Next (4*2)^2 elements contain the correlations.

        Returns
        -------
        rates : list
            Rates of the complex-valued variables defining the system. 
            First 2 elements contain the optical and mechanical modes of the 1st cavity.
            Next 2 elements contain the optical and mechanical modes of the 2nd cavity.
            Next (4*2)^2 elements contain the correlations.
        """

        # extract modes and correlations
        modes   = v[0:4]
        corrs   = np.real(v[4:]).reshape([8, 8])

        # mode rates
        mode_rates  = self.get_rates_modes(modes)

        # drift matrix
        A = self.get_A(modes)
        # noise matrix
        D = self.get_D()

        # quadrature correlation rate equation
        dcorrs_dt = A.dot(corrs) + corrs.dot(np.transpose(A)) + D

        # mirror matrix
        for i in range(len(dcorrs_dt)):
            for j in range(0, i):
                dcorrs_dt[i, j] = dcorrs_dt[j, i]

        # convert to 1D list and concatenate all rates
        rates = mode_rates + [np.complex(element) for element in dcorrs_dt.flatten()]

        return rates