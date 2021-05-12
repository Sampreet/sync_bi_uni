#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate a simple bidirectionally-coupled configuration of QOM systems."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-06-03'
__updated__ = '2021-05-12'

# dependencies
import numpy as np

# qom modules
from qom.systems import DODMSystem

class Bi00(DODMSystem):
    """Class to simulate a simple bidirectionally-coupled configuration of QOM systems.

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for Bi00."""
        
        # initialize super class
        super().__init__(params)

        # set attributes
        self.code = 'bi_00'
        self.name = 'Simple Bidirectional QOM System'  
        # default parameters
        self.params = {
            'A_l': params.get('A_l', 52.0),
            'Delta_0': params.get('Delta_0', 1.0),
            'delta': params.get('delta', 0.005),
            'g_0s': params.get('g_0s', [0.005, 0.005]),
            'gammas': params.get('gammas', [0.005, 0.005]),
            'kappas': params.get('kappas', [0.15, 0.15]),
            'lamb': params.get('lamb', 0.075),
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
        g_0s    = self.params['g_0s']
        gammas  = self.params['gammas']
        kappas  = self.params['kappas']
        lamb    = self.params['lamb']
        alphas  = [modes[0], modes[2]]
        betas   = [modes[1], modes[3]]

        # get frequencies
        Delta_0s, omega_ms = self.get_frequencies()

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
            self.A[4*i + 0][4*i + 0] = - kappas[i]
            self.A[4*i + 0][4*i + 1] = - Deltas[i]
            self.A[4*i + 0][4*i + 2] = - 2 * np.imag(gs[i])
            self.A[4*i + 0][4*(1 - i) + 1] = - lamb

            self.A[4*i + 1][4*i + 0] = Deltas[i]
            self.A[4*i + 1][4*i + 1] = - kappas[i]
            self.A[4*i + 1][4*i + 2] = 2 * np.real(gs[i])
            self.A[4*i + 1][4*(1 - i) + 0] = lamb

            self.A[4*i + 2][4*i + 2] = - gammas[i]
            self.A[4*i + 2][4*i + 3] = omega_ms[i]

            self.A[4*i + 3][4*i + 0] = 2 * np.real(gs[i])
            self.A[4*i + 3][4*i + 1] = 2 * np.imag(gs[i])
            self.A[4*i + 3][4*i + 2] = - omega_ms[i]
            self.A[4*i + 3][4*i + 3] = - gammas[i]

        return self.A

    def get_D(self):
        """Function to obtain the noise correlation matrix.
        
        Returns
        -------
        D : list
            Noise correlation matrix.
        """

        # extract frequently used variables
        gammas  = self.params['gammas']
        kappas  = self.params['kappas']
        n_ths   = self.params['n_ths']

        # noise correlation matrix
        if self.D is None or np.shape(self.D) != (8, 8):
            self.D = np.zeros([8, 8], dtype=np.float_)
        for i in range(2):
            self.D[4*i + 0][4*i + 0] = kappas[i]
            self.D[4*i + 1][4*i + 1] = kappas[i]
            self.D[4*i + 2][4*i + 2] = gammas[i] * (2 * n_ths[i] + 1)
            self.D[4*i + 3][4*i + 3] = gammas[i] * (2 * n_ths[i] + 1)

        return self.D

    def get_frequencies(self):
        """Function to obtain the mechanical frequencies and laser detunings.
        
        Returns
        -------
        Delta_0s : list
            Laser detunings.
        omega_ms : list
            Mechanical frequencies.
        """
        
        # extract frequently used variables
        delta       = self.params['delta']
        Delta_0     = self.params['Delta_0']
        omega_m     = self.params['omega_m']

        # mechanical frequencies
        omega_ms = [omega_m, omega_m + delta]
        # laser detunings
        Delta_0s = [Delta_0 * ele for ele in omega_ms]
            
        return Delta_0s, omega_ms

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
        g_0s    = self.params['g_0s']
        gammas  = self.params['gammas']
        kappas  = self.params['kappas']
        lamb    = self.params['lamb']
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
            dalpha_dts.append((- kappas[i] + 1j * Deltas[i]) * alphas[i] + 1j * lamb * alphas[1 - i] + A_l)
            dbeta_dts.append(1j * gs[i] * np.conjugate(alphas[i]) + (- gammas[i] - 1j * omega_ms[i]) * betas[i])

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
        n_ths    = self.params['n_ths']
 
        # initial mode values as 1D list
        u_0 = np.zeros(4, dtype=np.complex_).tolist()

        # initial quadrature correlations
        V_0 = np.zeros([8, 8], dtype=np.float_)
        for i in range(2):
            V_0[4*i + 0][4*i + 0] = 1 / 2
            V_0[4*i + 1][4*i + 1] = 1 / 2
            V_0[4*i + 2][4*i + 2] = (n_ths[i] + 1 / 2)
            V_0[4*i + 3][4*i + 3] = (n_ths[i] + 1 / 2)

        # convert to 1D list and concatenate all variables
        iv = u_0 + [np.complex_(element) for element in V_0.flatten()]

        return iv, None

    def ode_func(self, t, v):
        """Function for the rate equations of the modes and quadrature correlations.
        
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

        # extract the modes and correlations
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

        # mirror matrix about diagonal
        for i in range(len(dcorrs_dt)):
            for j in range(0, i):
                dcorrs_dt[i, j] = dcorrs_dt[j, i]

        # convert to 1D list and concatenate all rates
        rates = mode_rates + [np.complex(element) for element in dcorrs_dt.flatten()]

        return rates