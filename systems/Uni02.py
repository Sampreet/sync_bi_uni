#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate a simple unidirectionally-coupled configuration of identical QOM systems with adiabatically eliminated optical modes."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-07-06'
__updated__ = '2021-07-06'

# dependencies
import numpy as np

# qom modules
from qom.systems import BaseSystem

class Uni02(BaseSystem):
    """Class to simulate a simple unidirectionally-coupled configuration of identical QOM systems with adiabatically eliminated optical modes.

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for Uni02."""
        
        # initialize super class
        super().__init__(params)

        # set attributes
        self.code = 'uni_02'
        self.name = 'Unidirectional;y-coupled Identical Configuration with Adiabatically Eliminated Optical Modes'
        self.num_modes = 2
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
        A_l     = params[0]
        eta     = params[1]
        g_0s    = [params[2], params[3]]
        gammas  = [params[4], params[5]]
        kappas  = [params[6], params[7]]
        omegas  = [params[8], params[9]]
        alphas  = [modes[0], modes[1]]
        temp    = np.sqrt(eta * kappas[0] * kappas[1])

        # classical steady state values
        alphas  = list()
        alphas.append(A_l / (kappas[0] - 1j * omegas[0]))
        alphas.append(((np.sqrt(eta) + np.sqrt(1 - eta)) * A_l - 2 * temp * alphas[0]) / (kappas[1] - 1j * omegas[1]))

        # initialize lists
        Gs      = list()
        chis    = list()
        Gammas  = list()

        # effective coupling strengths
        Gs.append(g_0s[0] * alphas[0])
        Gs.append(g_0s[1] * alphas[1])
        # cross-oscillator coefficients
        chis.append(2 * np.conjugate(Gs[0]) * Gs[1] * eta / temp)
        chis.append(2 * np.conjugate(Gs[1]) * Gs[0] * eta / temp)
        # effective optomechanical damping
        Gammas.append(np.conjugate(Gs[0]) * Gs[0] / kappas[0])
        Gammas.append(np.conjugate(Gs[1]) * Gs[1] / kappas[1])

        # drift matrix
        if self.A is None or np.shape(self.A) != (4, 4):
            self.A = np.zeros([4, 4], dtype=np.float_)
        for i in range(2):
            self.A[2*i + 0][2*i + 0] = Gammas[i] - gammas[i]
            self.A[2*i + 1][2*i + 1] = Gammas[i] - gammas[i]
        self.A[2][0] = - np.real(chis[0])
        self.A[2][1] = np.imag(chis[0])
        self.A[3][0] = - np.imag(chis[0])
        self.A[3][1] = - np.real(chis[0])

        return self.A

    def get_ivc(self):
        """Function to obtain the initial values and constants required for the IVP.
        
        Returns
        -------
        iv : list
            Initial values of variables.
            First element contains the mechanical mode of first cavity.
            Next element contains the mechanical mode of second cavity.
            Next (2*2)^2 elements contain the correlations.

        c : list
            Constant parameters.
            First (2*2)^2 elements contain the noise matrix.
            Next element contains the laser amplitude.
            Next element contains the transmission loss.
            Next 2 elements contain the optomechanical coupling strengths.
            Next 2 elements contain the mechanical decay rates.
            Next 2 elements contain the optical decay rates.
            Next 2 elements contain the mechanical frequencies.
        """

        # extract frequently used variables
        A_l     = self.params['A_l']
        eta     = self.params['eta']
        g_0s    = self.params['g_0s']
        gammas  = self.params['gammas']
        kappas  = self.params['kappas']
        n_ths   = self.params['n_ths']
        omega_m = self.params['omega_m']
        temp    = np.sqrt(eta * kappas[0] * kappas[1])
 
        # initial mode values as 1D list
        modes_0 = np.zeros(2, dtype=np.complex_).tolist()

        # initial quadrature correlations
        corrs_0 = np.zeros([4, 4], dtype=np.float_)
        for i in range(2):
            corrs_0[2*i + 0][2*i + 0] = (n_ths[i] + 0.5)
            corrs_0[2*i + 1][2*i + 1] = (n_ths[i] + 0.5)

        # convert to 1D list and concatenate all variables
        iv = modes_0 + [np.complex_(element) for element in corrs_0.flatten()]

        # mechanical frequencies
        omegas = [omega_m, omega_m]

        # classical steady state values
        alpha_0 = A_l / (kappas[0] - 1j * omegas[0])
        alpha_1 = ((np.sqrt(eta) + np.sqrt(1 - eta)) * A_l - 2 * temp * alpha_0) / (kappas[1] - 1j * omegas[1])

        # initialize lists
        Gs      = list()
        etas    = list()
        chis    = list()
        Gammas  = list()

        # effective coupling strengths
        Gs.append(g_0s[0] * alpha_0)
        Gs.append(g_0s[1] * alpha_1)
        # noise coefficients
        etas.append(np.sqrt(2 / kappas[0]) * Gs[0])
        etas.append(np.sqrt(2 / kappas[1]) * Gs[1])
        # cross-oscillator coefficients
        chis.append(2 * np.conjugate(Gs[0]) * Gs[1] * eta / temp)
        chis.append(2 * np.conjugate(Gs[1]) * Gs[0] * eta / temp)
        # effective optomechanical damping
        Gammas.append(np.conjugate(Gs[0]) * Gs[0] / kappas[0])
        Gammas.append(np.conjugate(Gs[1]) * Gs[1] / kappas[1])

        # noise correlation matrix
        D = np.zeros([4, 4], dtype=np.float_)
        for i in range(2):
            D[2*i + 0][2*i + 0] = np.conjugate(etas[i]) * etas[i] / 2  + gammas[i] * (2 * n_ths[i] + 1)
            D[2*i + 1][2*i + 1] = np.conjugate(etas[i]) * etas[i] / 2  + gammas[i] * (2 * n_ths[i] + 1)
        temp_same = - np.sqrt(eta) / 2 * (np.imag(etas[0]) * np.imag(etas[1]) - np.sqrt(eta) * np.real(etas[0]) * np.real(etas[1]))
        temp_diff = np.sqrt(eta) / 2 * (np.imag(etas[0]) * np.real(etas[1]) / 2 - np.sqrt(eta) * np.real(etas[0]) * np.imag(etas[1]))
        D[0][2] = temp_same
        D[0][3] = temp_diff
        D[1][2] = - temp_diff
        D[1][3] = temp_same
        D[2][0] = temp_same
        D[2][1] = - temp_diff
        D[3][0] = temp_diff
        D[3][1] = temp_same
        
        # constant parameters
        params = [A_l] + \
            [eta] + \
            g_0s + \
            gammas + \
            kappas + \
            omegas

        # all constants
        c = D.flatten().tolist() + params

        return iv, c

    def get_mode_rates(self, modes, params, t):
        """Function to obtain the rates of the optical modes.

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
        eta     = params[1]
        kappas  = [params[6], params[7]]
        omegas  = [params[8], params[9]]
        alphas  = [modes[0], modes[1]]

        # initialize lists
        dalpha_dts  = list()

        # calculate rates
        for i in range(2):
            dalpha_dts.append((- kappas[i] + 1j * omegas[i]) * alphas[i])
        dalpha_dts[0] += A_l
        dalpha_dts[1] += - 2 * np.sqrt(eta * kappas[0] * kappas[1]) * alphas[0] + (np.sqrt(eta) + np.sqrt(1 - eta)) * A_l
        
        # rearrange per system
        mode_rates = [dalpha_dts[0], dalpha_dts[1]]

        return mode_rates