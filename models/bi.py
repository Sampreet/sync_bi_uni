#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Models to simulate a bidirectionally-coupled configuration of optomechanical systems."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-06-03'
__updated__ = '2020-09-01'

# dependencies
import numpy as np

class Model00(object):
    """Class containing the model and parameter generation function for the bidirectionally-coupled configuration of optomechanical cavities without transformation.

    The class inherits object.

    Attributes
    ----------
    NAME : str
        Name of the model
    
    CODE : str
        Short code for the model

    p : dict
        Parameters for the model.
    """
    
    # class attributes
    NAME = 'Simple Bidirectional'
    CODE = 'bi_00'
    p = {}

    def __init__(self, model_params):
        """Class constructor for Model.

        Parameters
        ----------
        model_params : dict
            Parameters for the model.
        """

        # initialize parent class
        super().__init__()

        # extract model params
        self.p = model_params

    def model_complex(self, t, v, c):
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
        A_l, lamb   = Params[5]
        # Next row onwards, noise correlations
        D = np.matrix(Params[6:]).reshape([4*2, 4*2])

        # effective values
        arr_Delta   = []
        arr_g       = []
        for i in range(2):
            arr_Delta.append(arr_Delta_0[i] + 2*arr_g_0[i]*np.real(arr_b[i]))
            arr_g.append(arr_g_0[i]*arr_a[i])

        # calculate rates
        arr_da_dt = []
        arr_db_dt = []
        for i in range(2):
            arr_da_dt.append((-arr_kappa[i] + 1j*arr_Delta[i])*arr_a[i] + 1j*lamb*arr_a[1-i] + A_l)
            arr_db_dt.append(1j*arr_g[i]*np.conjugate(arr_a[i]) + (-arr_gamma[i] - 1j*arr_omega_m[i])*arr_b[i])

        # initialize drift matrix
        A = np.zeros([4*2, 4*2], dtype='complex')
        for i in range(2):
            A[4*i + 0][4*i + 0] = -arr_kappa[i]
            A[4*i + 0][4*i + 1] = -arr_Delta[i]
            A[4*i + 0][4*i + 2] = -2*np.imag(arr_g[i])
            A[4*i + 0][4*(1-i) + 1] = - lamb

            A[4*i + 1][4*i + 0] = arr_Delta[i]
            A[4*i + 1][4*i + 1] = -arr_kappa[i]
            A[4*i + 1][4*i + 2] = 2*np.real(arr_g[i])
            A[4*i + 1][4*(1-i) + 0] = lamb

            A[4*i + 2][4*i + 2] = -arr_gamma[i]
            A[4*i + 2][4*i + 3] = arr_omega_m[i]

            A[4*i + 3][4*i + 0] = 2*np.real(arr_g[i])
            A[4*i + 3][4*i + 1] = 2*np.imag(arr_g[i])
            A[4*i + 3][4*i + 2] = -arr_omega_m[i]
            A[4*i + 3][4*i + 3] = -arr_gamma[i]

        # convert to matrix 
        A = np.matrix(A)

        # quadrature correlation rate equation
        dmat_Corr_dt = A.dot(mat_Corr) + mat_Corr.dot(np.transpose(A)) + D

        # convert to 1D list and concatenate all rates
        rates = [arr_da_dt[0], arr_db_dt[0], arr_da_dt[1], arr_db_dt[1]] + [np.complex(element) for row in dmat_Corr_dt.flatten().tolist() for element in row]

        # return concatenated list
        return rates

    def get_initial_values_and_constants(self):
        """Function to obtain the initial values and constants required for the IVP.
        
        Returns
        -------
        v : list
            Initial values of variables.

        c : list
            Constant parameters.
        """

        # extract frequently used variables
        # mechanical mode frequency
        omega_m     = self.p['omega_m']
        # cavity detuning
        Delta_0     = self.p['Delta_0']
        # optical mode decay rates
        arr_kappa   = self.p['kappa']
        # mechanical mode decay rates
        arr_gamma   = self.p['gamma']
        # coupling contants
        arr_g_0     = self.p['g_0']
        # mechanical detuning
        delta       = self.p['delta']
        # laser drive amplitude
        A_l         = self.p['A_l']
        # transmission loss coefficient
        lamb        = self.p['lamb']
        # mean thermal occupancy number
        arr_n_th    = self.p['n_th']

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

        # convert to 1D list and concatenate all constants
        c = arr_omega_m + \
            arr_Delta_0 + \
            arr_kappa + \
            arr_gamma + \
            arr_g_0 + \
            [A_l] + \
            [lamb] + \
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