#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate a unidirectionally-coupled configuration of QOM systems with Plus-Minus modes."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-01-28'
__updated__ = '2021-07-07'

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
        self.name = 'Unidirectionally-couple configuration with Plus-Minus Modes'
        
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
        # drift matrix
        self.A = None

    def get_A(self, modes, params, t):
        """Function to obtain the drift matrix.

        Parameters
        ----------
        modes : list
            Values of the modes.
        params : list
            Constant parameters.
        t : float
            Time at which the rates are calculated.
        
        Returns
        -------
        A : list
            Drift matrix.
        """

        # extract frequently used variables
        Delta_0s= [params[1], params[2]]
        eta     = params[3]
        g_0s    = [params[4], params[5]]
        gammas  = [params[6], params[7]]
        kappas  = [params[8], params[9]]
        omega_ms= [params[10], params[11]]
        alphas  = [modes[0], modes[2]]
        betas   = [modes[1], modes[3]]
        temp    = np.sqrt(eta * kappas[0] * kappas[1])

        # initialize lists
        Deltas  = list()
        gs      = list()

        # effective detunings
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

    def get_ivc(self):
        """Function to obtain the initial values and constants required for the IVP.
        
        Returns
        -------
        iv : list
            Initial values of variables.
            First element contains the optical mode of first cavity.
            Next element contains the mechanical mode of first cavity.
            Next element contains the optical mode of second cavity.
            Next element contains the mechanical mode of second cavity.
            Next (4*2)^2 elements contain the correlations.

        c : list
            Constant parameters.
            First (4*2)^2 elements contain the noise matrix.
            Next element contains the laser amplitude.
            Next 2 elements contain the laser detunings.
            Next element contains the transmission loss.
            Next 2 elements contain the optomechanical coupling strengths.
            Next 2 elements contain the mechanical decay rates.
            Next 2 elements contain the optical decay rates.
            Next 2 elements contain the mechanical frequencies.
        """

        # extract frequently used variables
        A_l     = self.params['A_l']
        Delta_0 = self.params['Delta_0']
        delta   = self.params['delta']
        eta     = self.params['eta']
        g_0s    = self.params['g_0s']
        gammas  = self.params['gammas']
        kappas  = self.params['kappas']
        n_ths   = self.params['n_ths']
        omega_m = self.params['omega_m']
        temp    = np.sqrt(eta * kappas[0] * kappas[1])
 
        # initial mode values as 1D list
        modes_0 = np.zeros(4, dtype=np.complex_).tolist()

        # initial quadrature correlations
        corrs_0 = np.zeros([8, 8], dtype=np.float_)
        for i in range(2):
            # alternate index 
            _ai = 1 if i == 0 else 0
            corrs_0[4*i + 0][4*i + 0] = 0.5
            corrs_0[4*i + 0][4*_ai + 0] = 0.5
            corrs_0[4*i + 1][4*i + 1] = 0.5
            corrs_0[4*i + 1][4*_ai + 1] = 0.5
            corrs_0[4*i + 2][4*i + 2] = (n_ths[i] + 0.5)
            corrs_0[4*i + 2][4*_ai + 2] = (n_ths[i] + 0.5)
            corrs_0[4*i + 3][4*i + 3] = (n_ths[i] + 0.5)
            corrs_0[4*i + 3][4*_ai + 3] = (n_ths[i] + 0.5)

        # convert to 1D list and concatenate all variables
        iv = modes_0 + [np.complex_(element) for element in corrs_0.flatten()]

        # noise correlation matrix
        D = np.zeros([8, 8], dtype=np.float_)
        for i in range(2):
            # sign of mode
            _sign = - 2 * (i - 0.5)
            # alternate index 
            _ai = 1 if i == 0 else 0
            # X
            D[4*i + 0][4*i + 0] = kappas[0] / 2 + kappas[1] / 2 + _sign * temp
            D[4*i + 0][4*_ai + 0] = kappas[0] / 2 - kappas[1] / 2
            # Y
            D[4*i + 1][4*i + 1] = kappas[0] / 2 + kappas[1] / 2 + _sign * temp
            D[4*i + 1][4*_ai + 1] = kappas[0] / 2 - kappas[1] / 2
            # Q
            D[4*i + 2][4*i + 2] = gammas[0] * (n_ths[0] + 0.5) + gammas[1] * (n_ths[1] + 0.5)
            D[4*i + 2][4*_ai + 2] = gammas[0] * (n_ths[0] + 0.5) + gammas[1] * (n_ths[1] + 0.5)
            # P
            D[4*i + 3][4*i + 3] = gammas[0] * (n_ths[0] + 0.5) + gammas[1] * (n_ths[1] + 0.5)
            D[4*i + 3][4*_ai + 3] = gammas[0] * (n_ths[0] + 0.5) + gammas[1] * (n_ths[1] + 0.5)

        # mechanical frequencies
        omega_ms = [omega_m, omega_m + delta]
        # laser detunings
        Delta_0s = omega_ms
        
        # constant parameters
        params = [A_l] + \
            Delta_0s + \
            [eta] + \
            g_0s + \
            gammas + \
            kappas + \
            omega_ms

        # all constants
        c = D.flatten().tolist() + params

        return iv, c

    def get_mode_rates(self, modes, params, t):
        """Function to obtain the rates of the optical and mechanical modes.

        Parameters
        ----------
        modes : list
            Values of the modes.
        params : list
            Constants parameters.
        t : float
            Time at which the rates are calculated.
        
        Returns
        -------
        mode_rates : list
            Rates for each mode.
        """
        
        # extract frequently used variables
        A_l     = params[0]
        Delta_0s= [params[1], params[2]]
        eta     = params[3]
        g_0s    = [params[4], params[5]]
        gammas  = [params[6], params[7]]
        kappas  = [params[8], params[9]]
        omega_ms= [params[10], params[11]]
        alphas  = [modes[0], modes[2]]
        betas   = [modes[1], modes[3]]

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
            dalpha_dts.append((- kappas[i] + 1j * Deltas[i]) * alphas[i])
            dbeta_dts.append(1j * gs[i] * np.conjugate(alphas[i]) + (- gammas[i] - 1j * omega_ms[i]) * betas[i])
        dalpha_dts[0] += A_l
        dalpha_dts[1] += - 2 * np.sqrt(eta * kappas[0] * kappas[1]) * alphas[0] + (np.sqrt(eta) + np.sqrt(1 - eta)) * A_l
        
        # rearrange per system
        mode_rates = [dalpha_dts[0], dbeta_dts[0], dalpha_dts[1], dbeta_dts[1]]

        return mode_rates