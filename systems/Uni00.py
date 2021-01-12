#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate a unidirectionally-coupled configuration of QOM systems."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-01-04'
__updated__ = '2021-01-12'

# dependencies
import numpy as np
import scipy.linalg as sl

# qom modules
from qom.systems import DODMSystem

# TODO: Variables

class Uni00(DODMSystem):
    """Class to simulate a unidirectionally-coupled configuration of QOM systems.

    Inherits :class:`qom.systems.DODMSystem`.

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for Uni00."""
        
        # initialize super class
        super().__init__(params)

        # update code and name
        self.code = 'sync_bi_uni_uni_00'
        self.name = 'Simple Unidirectional QOM System'

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
        A_l         = self.params['A_l']
        delta       = self.params['delta']
        Delta_0     = self.params['Delta_0']
        eta         = self.params['eta']
        arr_g_0     = self.params['g_0s']
        arr_gamma   = self.params['gammas']
        arr_kappa   = self.params['kappas']
        arr_n_th    = self.params['n_ths']
        omega_m     = self.params['omega_m']

        # update frequencies
        arr_omega_m = [omega_m, omega_m + delta]
        arr_Delta_0 = arr_omega_m
        if Delta_0 < 0:
            arr_Delta_0 = -1 * arr_omega_m

        # noise correlation matrix
        D = np.zeros([4*2, 4*2], dtype='float')
        # optical mode correlation relations
        for i in range(2):
            D[4*i + 0][4*i + 0] = arr_kappa[i]
            D[4*i + 1][4*i + 1] = arr_kappa[i]
            D[4*i + 2][4*i + 2] = arr_gamma[i]*(2*arr_n_th[i] + 1)
            D[4*i + 3][4*i + 3] = arr_gamma[i]*(2*arr_n_th[i] + 1)

        temp = np.sqrt(eta*arr_kappa[0]*arr_kappa[1])
        D[0][4] = temp
        D[1][5] = temp
        D[4][0] = temp
        D[5][1] = temp
        # # previous model
        # D[4][4] = eta*arr_kappa[1]
        # D[5][5] = eta*arr_kappa[1]

        # convert to 1D list and concatenate all constants
        c = arr_omega_m + \
            arr_Delta_0 + \
            arr_kappa + \
            arr_gamma + \
            arr_g_0 + \
            [A_l] + \
            [eta] + \
            D.flatten().tolist()
 
        # initial mode values as 1D list
        u_0 = np.zeros(2*2, dtype='complex').tolist()

        # initial quadrature correlations
        V_0 = np.zeros([4*2, 4*2], dtype='float')
        for i in range(2):
            V_0[4*i + 0][4*i + 0] = 1/2
            V_0[4*i + 1][4*i + 1] = 1/2
            V_0[4*i + 2][4*i + 2] = (arr_n_th[i] + 1/2)
            V_0[4*i + 3][4*i + 3] = (arr_n_th[i] + 1/2)

        # convert to 1D list and concatenate all variables
        v = u_0 + [np.complex(element) for element in V_0.flatten().tolist()]

        # return concatenated lists of variables and constants
        return v, c

    def ode_func(self, t, v, c):
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

        c : list
            Real-valued constants.
            First 2 elements contain the mechanical mode frequencies.
            Next 2 elements contain the detunings.
            Next 2 elements contain the optical mode decay rates.
            Next 2 elements contain the mechanical mode decay rates.
            Next 2 elements contain the intra-cavity coupling constants.
            Next element contains the laser drive amplitude.
            Next element contains the transmission loss coefficient.
            Next (4*2)^2 elements contain the noise correlations.

        Returns
        -------
        rates : list
            Rates of the complex-valued variables defining the system. 
            First 2 elements contain the optical and mechanical modes of the 1st cavity.
            Next 2 elements contain the optical and mechanical modes of the 2nd cavity.
            Next (4*2)^2 elements contain the correlations.
        """
        
        # extract variables
        U = np.array(v).flatten()
        # extract the optical modes
        arr_a = [U[0], U[2]]
        # extract the mechanical modes
        arr_b = [U[1], U[3]]
        # next element onwards, the correlations
        mat_Corr = np.matrix(np.real(U[4:])).reshape([4*2, 4*2])
        
        # extract constants
        Params = np.array(c).reshape([6 + 4*4*2, 2])
        # 1st row contains mechanical mode frequencies
        arr_omega_m = Params[0]
        # 2nd row contains detunings
        arr_Delta_0 = Params[1]
        # 3rd row contains optical mode decay rates
        arr_kappa   = Params[2]
        # 4th row contains mechanical mode decay rates
        arr_gamma   = Params[3]
        # 5th row contains coupling contants
        arr_g_0     = Params[4]
        # 6th row contains laser drive amplitude and transmission loss coefficient
        A_l, eta    = Params[5]
        # Next row onwards, noise correlations
        D = np.matrix(Params[6:]).reshape([4*2, 4*2])

        # effective detunings
        arr_Delta   = []
        arr_g       = []
        for i in range(2):
            arr_Delta.append(arr_Delta_0[i] + 2*arr_g_0[i]*np.real(arr_b[i]))
            arr_g.append(arr_g_0[i]*arr_a[i])
        # frequently used variables
        temp = np.sqrt(eta*arr_kappa[0]*arr_kappa[1])

        # calculate rates
        arr_da_dt = []
        arr_db_dt = []
        for i in range(2):
            arr_da_dt.append((-arr_kappa[i] + 1j*arr_Delta[i])*arr_a[i])
            arr_db_dt.append(1j*arr_g[i]*np.conjugate(arr_a[i]) + (-arr_gamma[i] - 1j*arr_omega_m[i])*arr_b[i])
        arr_da_dt[0] += A_l
        arr_da_dt[1] += -2*temp*arr_a[0] + (np.sqrt(eta) + np.sqrt(1 - eta))*A_l

        # initialize drift matrix
        A = np.zeros([4*2, 4*2], dtype='complex')
        for i in range(2):
            A[4*i + 0][4*i + 0] = -arr_kappa[i]
            A[4*i + 0][4*i + 1] = -arr_Delta[i]
            A[4*i + 0][4*i + 2] = -2*np.imag(arr_g[i])

            A[4*i + 1][4*i + 0] = arr_Delta[i]
            A[4*i + 1][4*i + 1] = -arr_kappa[i]
            A[4*i + 1][4*i + 2] = 2*np.real(arr_g[i])

            A[4*i + 2][4*i + 2] = -arr_gamma[i]
            A[4*i + 2][4*i + 3] = arr_omega_m[i]

            A[4*i + 3][4*i + 0] = 2*np.real(arr_g[i])
            A[4*i + 3][4*i + 1] = 2*np.imag(arr_g[i])
            A[4*i + 3][4*i + 2] = -arr_omega_m[i]
            A[4*i + 3][4*i + 3] = -arr_gamma[i]
        A[4][0] = -2*temp
        A[5][1] = -2*temp

        # convert to numpy matrix 
        A = np.matrix(A)

        # quadrature correlation rate equation
        dmat_Corr_dt = A.dot(mat_Corr) + mat_Corr.dot(np.transpose(A)) + D

        # # account for numerical error
        # dmat_Corr_dt = (dmat_Corr_dt + np.transpose(dmat_Corr_dt)) / 2

        # mirror matrix
        for i in range(len(dmat_Corr_dt)):
            for j in range(0, i):
                dmat_Corr_dt[i, j] = dmat_Corr_dt[j, i]

        # convert to 1D list and concatenate all rates
        rates = [arr_da_dt[0], arr_db_dt[0], arr_da_dt[1], arr_db_dt[1]] + [np.complex(element) for row in dmat_Corr_dt.flatten().tolist() for element in row]

        # return concatenated list
        return rates

    def ode_func_modes(self, t, u, c):
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

        c : list
            Real-valued constants.
            First 2 elements contain the mechanical mode frequencies.
            Next 2 elements contain the detunings.
            Next 2 elements contain the optical mode decay rates.
            Next 2 elements contain the mechanical mode decay rates.
            Next 2 elements contain the intra-cavity coupling constants.
            Next element contains the laser drive amplitude.
            Next element contains the transmission loss coefficient.
            Next (4*2)^2 elements contain the noise correlations.

        Returns
        -------
        rates : list
            Rates of the complex-valued variables defining the system. 
            First 2 elements contain the optical and mechanical modes of the 1st cavity.
            Next 2 elements contain the optical and mechanical modes of the 2nd cavity.
            Next (4*2)^2 elements contain the correlations.
        """
        
        # extract the optical modes
        arr_a = [u[0], u[2]]
        # extract the mechanical modes
        arr_b = [u[1], u[3]]
        
        # extract constants
        Params = np.array(c).reshape([6 + 4*4*2, 2])
        # 1st row contains mechanical mode frequencies
        arr_omega_m = Params[0]
        # 2nd row contains detunings
        arr_Delta_0 = Params[1]
        # 3rd row contains optical mode decay rates
        arr_kappa   = Params[2]
        # 4th row contains mechanical mode decay rates
        arr_gamma   = Params[3]
        # 5th row contains coupling contants
        arr_g_0     = Params[4]
        # 6th row contains laser drive amplitude and transmission loss coefficient
        A_l, eta    = Params[5]

        # effective detunings
        arr_Delta   = []
        arr_g       = []
        for i in range(2):
            arr_Delta.append(arr_Delta_0[i] + 2*arr_g_0[i]*np.real(arr_b[i]))
            arr_g.append(arr_g_0[i]*arr_a[i])
        # frequently used variables
        temp = np.sqrt(eta*arr_kappa[0]*arr_kappa[1])

        # calculate rates
        arr_da_dt = []
        arr_db_dt = []
        for i in range(2):
            arr_da_dt.append((-arr_kappa[i] + 1j*arr_Delta[i])*arr_a[i])
            arr_db_dt.append(1j*arr_g[i]*np.conjugate(arr_a[i]) + (-arr_gamma[i] - 1j*arr_omega_m[i])*arr_b[i])
        arr_da_dt[0] += A_l
        arr_da_dt[1] += -2*temp*arr_a[0] + (np.sqrt(eta) + np.sqrt(1 - eta))*A_l

        # convert to 1D list and concatenate all rates
        rates = [arr_da_dt[0], arr_db_dt[0], arr_da_dt[1], arr_db_dt[1]]

        # return concatenated list
        return rates

    def ode_func_corrs(self, t, v, c):
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

        c : list
            Real-valued constants.
            First 2 elements contain the mechanical mode frequencies.
            Next 2 elements contain the detunings.
            Next 2 elements contain the optical mode decay rates.
            Next 2 elements contain the mechanical mode decay rates.
            Next 2 elements contain the intra-cavity coupling constants.
            Next element contains the laser drive amplitude.
            Next element contains the transmission loss coefficient.
            Next (4*2)^2 elements contain the noise correlations.

        Returns
        -------
        rates : list
            Rates of the complex-valued variables defining the system. 
            First 2 elements contain the optical and mechanical modes of the 1st cavity.
            Next 2 elements contain the optical and mechanical modes of the 2nd cavity.
            Next (4*2)^2 elements contain the correlations.
        """

        # next element onwards, the correlations
        mat_Corr = np.matrix(np.real(v)).reshape([4*2, 4*2])
        
        # extract constants
        Params = np.array(c).reshape([6 + 4*4*2 + 2, 2])
        # 1st row contains mechanical mode frequencies
        arr_omega_m = Params[0]
        # 2nd row contains detunings
        arr_Delta_0 = Params[1]
        # 3rd row contains optical mode decay rates
        arr_kappa   = Params[2]
        # 4th row contains mechanical mode decay rates
        arr_gamma   = Params[3]
        # 5th row contains coupling contants
        arr_g_0     = Params[4]
        # 6th row contains laser drive amplitude and transmission loss coefficient
        A_l, eta    = Params[5]
        # Next row onwards, noise correlations
        D = np.matrix(Params[6:6 + 4*4*2]).reshape([4*2, 4*2])
        # extract the optical modes
        arr_a = [Params[6 + 4*4*2][0], Params[6 + 4*4*2 + 1][0]]
        # extract the mechanical modes
        arr_b = [Params[6 + 4*4*2][1], Params[6 + 4*4*2 + 1][1]]

        # effective detunings
        arr_Delta   = []
        arr_g       = []
        for i in range(2):
            arr_Delta.append(arr_Delta_0[i] + 2*arr_g_0[i]*np.real(arr_b[i]))
            arr_g.append(arr_g_0[i]*arr_a[i])
        # frequently used variables
        temp = np.sqrt(eta*arr_kappa[0]*arr_kappa[1])

        # initialize drift matrix
        A = np.zeros([4*2, 4*2], dtype='float')
        for i in range(2):
            A[4*i + 0][4*i + 0] = -arr_kappa[i]
            A[4*i + 0][4*i + 1] = -arr_Delta[i]
            A[4*i + 0][4*i + 2] = -2*np.imag(arr_g[i])

            A[4*i + 1][4*i + 0] = arr_Delta[i]
            A[4*i + 1][4*i + 1] = -arr_kappa[i]
            A[4*i + 1][4*i + 2] = 2*np.real(arr_g[i])

            A[4*i + 2][4*i + 2] = -arr_gamma[i]
            A[4*i + 2][4*i + 3] = arr_omega_m[i]

            A[4*i + 3][4*i + 0] = 2*np.real(arr_g[i])
            A[4*i + 3][4*i + 1] = 2*np.imag(arr_g[i])
            A[4*i + 3][4*i + 2] = -arr_omega_m[i]
            A[4*i + 3][4*i + 3] = -arr_gamma[i]
        A[4][0] = -2*temp
        A[5][1] = -2*temp

        # convert to numpy matrix 
        A = np.matrix(A)

        # quadrature correlation rate equation
        dmat_Corr_dt = A.dot(mat_Corr) + mat_Corr.dot(np.transpose(A)) + D

        # # average out upper and lower triangular matrices
        # dmat_Corr_dt = (dmat_Corr_dt + np.transpose(dmat_Corr_dt)) / 2

        # mirror matrix about diagonal
        for i in range(len(dmat_Corr_dt)):
            for j in range(0, i):
                dmat_Corr_dt[i, j] = dmat_Corr_dt[j, i]

        # convert to 1D list and concatenate all rates
        rates = [np.real(element) for row in dmat_Corr_dt.flatten().tolist() for element in row]

        # return concatenated list
        return rates

    def get_measure_average(self, solver_params, plot=False, plotter_params=None):
        """Method to obtain the average value of a measure.
        
        Parameters
        ----------
        solver_params : dict
            Parameters for the solver.
        plot: bool, optional
            Option to plot the measures. Requires `plotter_params` parameter if `True`.
        plotter_params: dict, optional
            Parameters for the plotter.
        
        Returns
        -------
        m_avg : float
            Average value.
        """

        # get measure
        M = self.get_dynamics_measure(solver_params, self.ode_func_modes, self.ivc_func, self.ode_func_corrs, plot, plotter_params)

        # calculate average
        m_avg = np.mean(M)

        return m_avg

    def get_measure_pearson(self, solver_params, plot=False, plotter_params=None):
        """Method to obtain the Pearson correlator value of a measure.
        
        Parameters
        ----------
        solver_params : dict
            Parameters for the solver.
        plot: bool, optional
            Option to plot the measures. Requires `plotter_params` parameter if `True`.
        plotter_params: dict, optional
            Parameters for the plotter.
        
        Returns
        -------
        C_P : float
            Pearson correlator.
        """

        # get measure
        M = self.get_dynamics_measure(solver_params, self.ode_func_modes, self.ivc_func, self.ode_func_corrs, plot, plotter_params)

        # frequently used variables
        _dim = len(M)

        # get means
        _mean_ii = np.mean([M[i][0] for i in range(_dim)])
        _mean_ij = np.mean([M[i][1] for i in range(_dim)])
        _mean_jj = np.mean([M[i][2] for i in range(_dim)])

        # calculate average
        C_P = _mean_ij / np.sqrt(_mean_ii * _mean_jj)

        return C_P

    def get_drift_matrix_eig(self, arr_alpha, arr_beta):
        """Function to obtain the eigenvalues of the drift matrix.

        Parameters
        ----------
        arr_alpha : list
            Values of the optical mode.
        
        arr_beta : list
            Values of the mechanical mode.
        
        Returns
        -------
        eig : list
            Eigenvalues of the drift matrix.
        """

        # get drift matrix
        A = self.get_drift_matrix(arr_alpha, arr_beta)

        # eigenvalues of the drift matrix
        return np.linalg.eig(A)


    def get_drift_matrix(self, arr_alpha, arr_beta):
        """Function to obtain the drift matrix.

        Parameters
        ----------
        arr_alpha : list
            Values of the optical mode.
        
        arr_beta : list
            Values of the mechanical mode.
        
        Returns
        -------
        A : list
            Drift matrix.
        """

        # extract frequently used variables
        delta       = self.params['delta']
        Delta_0     = self.params['Delta_0']
        eta         = self.params['eta']
        arr_g_0     = self.params['g_0s']
        arr_gamma   = self.params['gammas']
        arr_kappa   = self.params['kappas']
        omega_m     = self.params['omega_m']

        # update frequencies
        arr_omega_m = [omega_m, omega_m + delta]
        arr_Delta_0 = arr_omega_m
        if Delta_0 < 0:
            arr_Delta_0 = -1 * arr_omega_m

        # effective detunings
        arr_Delta   = []
        arr_g       = []
        for i in range(2):
            arr_Delta.append(arr_Delta_0[i] + 2*arr_g_0[i]*np.real(arr_beta[i]))
            arr_g.append(arr_g_0[i]*arr_alpha[i])

        # initialize drift matrix
        A = np.zeros([4*2, 4*2], dtype='complex')
        for i in range(2):
            A[4*i + 0][4*i + 0] = -arr_kappa[i]
            A[4*i + 0][4*i + 1] = -arr_Delta[i]
            A[4*i + 0][4*i + 2] = -2*np.imag(arr_g[i])

            A[4*i + 1][4*i + 0] = arr_Delta[i]
            A[4*i + 1][4*i + 1] = -arr_kappa[i]
            A[4*i + 1][4*i + 2] = 2*np.real(arr_g[i])

            A[4*i + 2][4*i + 2] = -arr_gamma[i]
            A[4*i + 2][4*i + 3] = arr_omega_m[i]

            A[4*i + 3][4*i + 0] = 2*np.real(arr_g[i])
            A[4*i + 3][4*i + 1] = 2*np.imag(arr_g[i])
            A[4*i + 3][4*i + 2] = -arr_omega_m[i]
            A[4*i + 3][4*i + 3] = -arr_gamma[i]
        A[4][0] = -2*np.sqrt(eta*arr_kappa[0]*arr_kappa[1])
        A[5][1] = -2*np.sqrt(eta*arr_kappa[0]*arr_kappa[1])

        # drift matrix
        return A

    def get_antisync_condition(self, arr_alpha):
        delta       = self.params['delta']
        eta         = self.params['eta']
        arr_g_0     = self.params['g_0s']
        arr_gamma   = self.params['gammas']
        arr_kappa   = self.params['kappas']

        arr_chi     = []
        arr_Gamma   = []
        for i in range(2):
            arr_chi.append(2 * arr_alpha[i] * arr_g_0[i] * np.conjugate(arr_alpha[(i + 1) % 2]) * arr_g_0[(i + 1) % 2] * np.sqrt(eta / arr_kappa[i] * arr_kappa[(i + 1) % 2]))
            arr_Gamma.append(np.abs(arr_alpha[i])**2 * arr_g_0[i]**2 / arr_kappa[i])

        print('Gamma_1 = {0:6.6f}\tGamma_2 = {1:6.6f}'.format(arr_Gamma[0], arr_Gamma[1]))

        # cond = (arr_Gamma[1] - arr_gamma[1])**2 + delta**2

        # cond = np.abs(arr_chi[1])**2 / ((arr_Gamma[1] - arr_gamma[1])**2 + delta**2)

        cond = (arr_Gamma[1] - arr_gamma[1]) * ((arr_Gamma[1] - arr_gamma[1] + arr_Gamma[0] - arr_gamma[0])**2 + delta**2)

        # cond = np.abs(arr_chi[1])**2 * (arr_Gamma[1] - arr_gamma[1] + arr_Gamma[0] - arr_gamma[0]) / (arr_Gamma[1] - arr_gamma[1]) / ((arr_Gamma[1] - arr_gamma[1] + arr_Gamma[0] - arr_gamma[0])**2 + delta**2)

        return cond

    def get_num_modes_approx(self, arr_alpha):
        delta       = self.params['delta']
        eta         = self.params['eta']
        arr_g_0     = self.params['g_0s']
        arr_gamma   = self.params['gammas']
        arr_kappa   = self.params['kappas']

        arr_Gamma   = []
        for i in range(2):
            arr_Gamma.append(np.abs(arr_alpha[i])**2 * arr_g_0[i]**2 / arr_kappa[i])
        
        chi = 2 * np.sqrt(arr_Gamma[0] * arr_Gamma[1] * eta)

        A = [   [   arr_Gamma[0] - arr_gamma[0],    0,  0,      0       ],
                [   0,  arr_Gamma[0] - arr_gamma[0],    0,      0       ],
                [   - chi,  0,  arr_Gamma[1] - arr_gamma[1],    delta   ],
                [   0,  - chi,  - delta,    arr_Gamma[1] - arr_gamma[1] ]   ]

        D = [   [   arr_Gamma[0] + arr_gamma[0],    0,  - chi / 2,  0   ],
                [   0,  arr_Gamma[0] + arr_gamma[0],    0,  - chi / 2   ],
                [   - chi / 2,  0,  arr_Gamma[1] + arr_gamma[1],    0   ],
                [   0,  - chi / 2,  0,  arr_Gamma[1] + arr_gamma[1]     ]   ]

        V = sl.solve_lyapunov(np.array(A), -1 * np.array(D))

        num_b1 = (V[0, 0] + V[1, 1] - 1) / 2
        num_b2 = (V[2, 2] + V[3, 3] - 1) / 2

        return np.real(num_b1), np.real(num_b2)