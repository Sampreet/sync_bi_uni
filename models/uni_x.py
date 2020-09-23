#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Models to simulate a unidirectionally-coupled configuration of optomechanical systems."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-09-21'
__updated__ = '2020-09-22'

# dependencies
import numpy as np

class Model00():
    """Class containing the model and parameter generation function for the unidirectionally-coupled configuration of optomechanical cavities without transformation.

    Properties
    ----------
    name : str
        Name of the model
    
    code : str
        Short code for the model

    params : dict
        Base parameters for the model.
    """

    def __init__(self, model_data):
        """Class constructor for Model.

        Parameters
        ----------
        model_data : dict
            Data for the model.
        """

        self.name = model_data['name']
        self.code = model_data['code']
        self.params = model_data['params']

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, params):
        self.__params = params

    def f_multi_complex(self, t, v, c):
        """Model function for the rate equations of the modes and correlations.
        
        The variables are complex-valued, hence the model requires a complex-valued integrator.
        
        Parameters
        ----------
        t : float
            Time at which the rate is calculated.

        v : list
            Complex-valued variables defining the systems: 
                First 2 elements contain the optical and mechanical modes of the 1st cavity.
                Next 2 elements contain the optical and mechanical modes of the 2nd cavity.
                Next (4*2)^2 elements contain the correlations.

        c : dict
            Real-valued constants:
                n_s : int
                    Number of systems.
                
                n_m : int
                    Number of modes in each system.

                params : list
                    Parameters of each system:
                        First 2 elements are mechanical frequencies.
                        Next 2 elements are detunings.
                        Next 2 elements are optical mode decay rates.
                        Next 2 elements are mechanical mode decay rates.
                        Next 2 elements are intra-cavity coupling constants.
                        Next element is laser drive amplitude.
                        Next element is transmission loss coefficient.

        Returns
        -------
        rates : list
            Rates of the complex-valued variables for the systems:
                First 2 elements contain the optical and mechanical modes of the 1st cavity.
                Next 2 elements contain the optical and mechanical modes of the 2nd cavity.
                Next (4*2)^2 elements contain the correlations.
        """
        # constants
        _n_s = c['n_s']
        _n_c = c['n_c']
        _n_m = c['n_m']
        _params = c['params']
        _Coeffs = c['Coeffs']
        _consts = c['consts']
        _Drifts = c['Drifts']
        _Noises = c['Noises']
        _idx = {
            'omega_ms': 0,
            'Delta_0s': 2,
            'kappas': 4,
            'gammas': 6,
            'g_0s': 8,
            'A_l': 10,
            'eta': 11
        }

        # variables
        _v = np.array(v).reshape((_n_s, _n_m * (4 * _n_m + 1)))
        _modes = _v[:, : _n_m].reshape((_n_s, _n_m))
        _Corrs = _v[:, _n_m :].reshape((_n_s, 2 * _n_m, 2 * _n_m))

        for i in range(_n_s):
            # populate matrices
            for j in range(_n_c):
                # effective detuning
                _Delta = _params[i][_idx['Delta_0s'] + j] + 2 * _params[i][_idx['g_0s'] + j] * np.real(_modes[i][2 * j + 1])
                # effective coupling
                _g = _params[i][_idx['g_0s'] + j] * _modes[i][2 * j + 0]

                # optical mode
                _Coeffs[i][2 * j + 0][2 * j + 0] = - _params[i][_idx['kappas']] + 1j * _Delta
                # optical position quadrature
                _Drifts[i][4 * j + 0][4 * j + 1] = - _Delta
                _Drifts[i][4 * j + 0][4 * j + 2] = - 2 * np.imag(_g)
                # optical momentum quadrature
                _Drifts[i][4 * j + 1][4 * j + 0] = _Delta
                _Drifts[i][4 * j + 1][4 * j + 2] = 2 * np.real(_g)

                # mechanical mode
                _Coeffs[i][2 * j + 1][2 * j + 0] = 1j * np.conjugate(_g)
                # mechanical momentum quadrature
                _Drifts[i][4 * j + 3][4 * j + 0] = 2 * np.real(_g)
                _Drifts[i][4 * j + 3][4 * j + 1] = 2 * np.imag(_g)

        # # tensordot
        # rate_modes = np.tensordot(_Coeffs, _modes, axes=((2,), (1,))).diagonal(axis1=0, axis2=2).transpose() + _consts
        # AV = np.tensordot(_Drifts, _Corrs, axes=((2,), (1,))).diagonal(axis1=0, axis2=2).transpose(2, 0, 1)
        # VAT = np.tensordot(_Corrs, np.transpose(_Drifts, (0, 2, 1)), axes=((2,), (1,))).diagonal(axis1=0, axis2=2).transpose(2, 0, 1)
        # rate_Corrs = (AV + VAT + _Noises).reshape((_n_s, 4 * _n_m * _n_m))

        # list comprehension
        rate_modes = [np.dot(_Coeffs[i], _modes[i]) + _consts[i] for i in range(_n_s)]
        rate_Corrs = [(np.dot(_Drifts[i], _Corrs[i]) + _Corrs[i].dot(np.transpose(_Drifts[i])) + _Noises[i]).ravel() for i in range(_n_s)]

        # # map
        # mode_rate = lambda M, m, n: np.dot(M, m) + n
        # corr_rate = lambda A, V, D: (np.dot(A, V) + np.dot(V, np.transpose(A)) + D).ravel()
        # rate_modes = list(map(mode_rate, _Coeffs, _modes, _consts))
        # rate_Corrs = list(map(corr_rate, _Drifts, _Corrs, _Noises))

        rates = np.zeros((_n_s, _n_m * (4 * _n_m + 1)), dtype='complex')
        rates[:, : _n_m] = rate_modes
        rates[:, _n_m :] = rate_Corrs

        return rates.ravel().tolist()

    def get_ivc_multi(self, var_params=None):
        """Function to obtain the initial values and constants required for the IVP.

        Parameters
        ----------
        var_params : dict
            The variable parameter of the model.

        Returns
        -------
        v : list
            Initial value of the variables.
        
        c : dict
            Constant parameters.
        """

        # TODO: Handle indexing.
        # TODO: Handle multiple variables.

        # extractly frequently used variables
        if var_params:
            _dim = [len(var_params[key]) for key in var_params]
            _n_s = np.prod(_dim)
        else:
            _n_s = 1
        _n_c = 2    # number of cavities
        _n_m = 4    # number of modes
        _n_p = 14   # number of parameters

        # variables
        _v = list()
        # constants
        _c = dict()
        _c['n_s'] = _n_s
        _c['n_c'] = _n_c
        _c['n_m'] = _n_m
        _idx = {
            'omega_ms': 0,
            'Delta_0s': 2,
            'kappas': 4,
            'gammas': 6,
            'g_0s': 8,
            'A_l': 10,
            'eta': 11,
            'n_ths':12
        }

        # parameters
        _params = np.zeros((_n_s, _n_p))

        # mechanical frequencies
        _omega_m = self.params['omega_m']
        if 'delta' in var_params:
            _deltas = var_params['delta']
            _omega_ms = np.array([_omega_m * np.ones(len(_deltas)), _omega_m + np.array(_deltas)]).transpose()
        else: 
            _delta = self.params['delta']
            _omega_ms = np.array([_omega_m, _omega_m + _delta])
        _params[:, _idx['omega_ms'] : _idx['omega_ms'] + _n_c] = _omega_ms

        # detunings
        _Delta_0s = self.params['Delta_0'] * _omega_ms
        _params[:, _idx['Delta_0s'] : _idx['Delta_0s'] + _n_c] = _Delta_0s

        # optical mode decay rates
        _params[:, _idx['kappas'] : _idx['kappas'] + _n_c] = self.params['kappas']

        # optical mode decay rates
        _params[:, _idx['gammas'] : _idx['gammas'] + _n_c] = self.params['gammas']

        # optical mode decay rates
        _params[:,  _idx['g_0s'] : _idx['g_0s'] + _n_c] = self.params['g_0s']

        # laser drive amplitude
        _params[:, _idx['A_l']] = self.params['A_l']

        # transmission loss coefficient
        if 'eta' in var_params:
            _eta = np.array(var_params['eta'])
        else:
            _eta = self.params['eta']
        _params[:, _idx['eta']] = _eta        

        # thermal phonon numbers
        _params[:, _idx['n_ths'] : _idx['n_ths'] + _n_c] = self.params['n_ths']  

        # initialize lists
        _Coeffs = list()
        _consts = list()
        _Drifts = list()
        _Noises = list()

        # populate
        for i in range(_n_s):
            # modes
            m = np.zeros((_n_m), dtype='complex')
            # quadrature correlations
            V = np.zeros((2 * _n_m, 2 * _n_m), dtype='complex')
            # coefficient matrix
            M = np.zeros((_n_m, _n_m)).tolist()
            # drift matrix
            A = np.zeros((2 * _n_m, 2 * _n_m)).tolist()
            # noise matrix
            D = np.zeros((2 * _n_m, 2 * _n_m)).tolist()

            # populate matrices
            for j in range(_n_c):
                # effective detuning
                _Delta = _params[i][_idx['Delta_0s'] + j] + 2 * _params[i][_idx['g_0s'] + j] * np.real(m[2 * j + 1])
                # effective coupling
                _g = _params[i][_idx['g_0s'] + j] * m[2 * j + 0]

                # optical mode
                M[2 * j + 0][2 * j + 0] = - _params[i][_idx['kappas']] + 1j * _Delta
                # optical position quadrature
                A[4 * j + 0][4 * j + 0] = - _params[i][_idx['kappas'] + j]
                A[4 * j + 0][4 * j + 1] = - _Delta
                A[4 * j + 0][4 * j + 2] = - 2 * np.imag(_g)
                # optical momentum quadrature
                A[4 * j + 1][4 * j + 0] = _Delta
                A[4 * j + 1][4 * j + 1] = - _params[i][_idx['kappas'] + j]
                A[4 * j + 1][4 * j + 2] = 2 * np.real(_g)

                # mechanical mode
                M[2 * j + 1][2 * j + 0] = 1j * np.conjugate(_g)
                M[2 * j + 1][2 * j + 1] = - _params[i][_idx['gammas'] + j] - 1j * _params[i][_idx['omega_ms'] + j]
                # mechanical position quadrature
                A[4 * j + 2][4 * j + 2] = - _params[i][_idx['gammas'] + j]
                A[4 * j + 2][4 * j + 3] = _params[i][_idx['omega_ms'] + j]
                # mechanical momentum quadrature
                A[4 * j + 3][4 * j + 0] = 2 * np.real(_g)
                A[4 * j + 3][4 * j + 1] = 2 * np.imag(_g)
                A[4 * j + 3][4 * j + 2] = - _params[i][_idx['omega_ms'] + j]
                A[4 * j + 3][4 * j + 3] = - _params[i][_idx['gammas'] + j]

                # correlations
                V[4 * j + 0][4 * j + 0] = 1 / 2
                V[4 * j + 1][4 * j + 1] = 1 / 2
                V[4 * j + 2][4 * j + 2] = (2 * _params[i][_idx['n_ths'] + j] + 1) / 2
                V[4 * j + 3][4 * j + 3] = (2 * _params[i][_idx['n_ths'] + j] + 1) / 2

                # noises
                D[4 * j + 0][4 * j + 0] = _params[i][_idx['kappas'] + j]
                D[4 * j + 1][4 * j + 1] = _params[i][_idx['kappas'] + j]
                D[4 * j + 2][4 * j + 2] = _params[i][_idx['gammas'] + j] * (2 * _params[i][_idx['n_ths'] + j] + 1)
                D[4 * j + 3][4 * j + 3] = _params[i][_idx['gammas'] + j] * (2 * _params[i][_idx['n_ths'] + j] + 1)

            # additional elements
            temp = np.sqrt(_params[i][_idx['eta']] * _params[i][_idx['kappas']] * _params[i][_idx['kappas'] + 1])
            # second optical mode
            M[2][0] = - 2 * temp
            # second optical position quadrature
            A[4][0] = - 2 * temp
            # second optical momentum quadrature
            A[5][1] = - 2 * temp
            # noises
            D[0][4] = temp
            D[1][5] = temp
            D[4][0] = temp
            D[5][1] = temp

            # update lists
            _v += m.ravel().tolist() + V.ravel().tolist()
            _Coeffs.append(M)
            _consts.append([_params[i][_idx['A_l']], 0, (np.sqrt(_params[i][_idx['eta']]) + np.sqrt(1 - _params[i][_idx['eta']])) * _params[i][_idx['A_l']], 0])
            _Drifts.append(A)
            _Noises.append(D)

        # update constants
        _c['params'] = _params
        _c['Coeffs'] = _Coeffs
        _c['consts'] = _consts
        _c['Drifts'] = _Drifts
        _c['Noises'] = _Noises

        return _v, _c
