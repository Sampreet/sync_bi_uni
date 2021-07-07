#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate a simple unidirectionally-coupled configuration of QOM systems."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-01-04'
__updated__ = '2021-07-07'

# dependencies
import numpy as np

# qom modules
from qom.systems import DODMSystem

class Uni00(DODMSystem):
    """Class to simulate a simple unidirectionally-coupled configuration of QOM systems.

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for Uni00."""
        
        # initialize super class
        super().__init__(params)

        # set attributes
        self.code = 'uni_00'
        self.name = 'Unidirectionally-coupled Configuration'
        # set parameters
        self.params = {
            'A_l': params.get('A_l', 52.0),
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
        A : numpy.ndarray
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
            self.A[4*i + 0][4*i + 0] = - kappas[i]
            self.A[4*i + 0][4*i + 1] = - Deltas[i]
            self.A[4*i + 0][4*i + 2] = - 2 * np.imag(gs[i])

            self.A[4*i + 1][4*i + 0] = Deltas[i]
            self.A[4*i + 1][4*i + 1] = - kappas[i]
            self.A[4*i + 1][4*i + 2] = 2 * np.real(gs[i])

            self.A[4*i + 2][4*i + 2] = - gammas[i]
            self.A[4*i + 2][4*i + 3] = omega_ms[i]

            self.A[4*i + 3][4*i + 0] = 2 * np.real(gs[i])
            self.A[4*i + 3][4*i + 1] = 2 * np.imag(gs[i])
            self.A[4*i + 3][4*i + 2] = - omega_ms[i]
            self.A[4*i + 3][4*i + 3] = - gammas[i]
        self.A[4][0] = - 2 * temp
        self.A[5][1] = - 2 * temp

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
            corrs_0[4*i + 0][4*i + 0] = 0.5
            corrs_0[4*i + 1][4*i + 1] = 0.5
            corrs_0[4*i + 2][4*i + 2] = (n_ths[i] + 0.5)
            corrs_0[4*i + 3][4*i + 3] = (n_ths[i] + 0.5)

        # convert to 1D list and concatenate all variables
        iv = modes_0 + [np.complex_(element) for element in corrs_0.flatten()]

        # noise correlation matrix
        D = np.zeros([8, 8], dtype=np.float_)
        for i in range(2):
            D[4*i + 0][4*i + 0] = kappas[i]
            D[4*i + 1][4*i + 1] = kappas[i]
            D[4*i + 2][4*i + 2] = gammas[i] * (2 * n_ths[i] + 1)
            D[4*i + 3][4*i + 3] = gammas[i] * (2 * n_ths[i] + 1)
        D[0][4] = temp
        D[1][5] = temp
        D[4][0] = temp
        D[5][1] = temp

        # mechanical frequencies
        omega_ms = [omega_m, omega_m + delta]
        # laser detunings
        Delta_0s = [Delta_0 * e for e in omega_ms]
        
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