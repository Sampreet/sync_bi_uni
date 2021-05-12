# dependencies
import numpy as np

# qom modules
from qom.ui import init_log
from qom.loopers import XLooper, XYLooper, XYZLooper

def wrap_looper(SystemClass, params, func_name, looper_name, file_path, plot=False, width=5.0, height=5.0):
    """Function to wrap loopers.
    
    Parameters
    ----------
    SystemClass : :class:`qom.systems.*`
        Class containing the system.
    params : dict
        Parameters for the system.
    func_name : str
        Name of the function to loop. Available functions are:
            'measure_average': Average measure (fallback).
            'measure_pearson': Pearson synchronization measure.
            'TLE': Transverse Lyapunov exponents.
    looper_name : str
        Name of the looper. Available loopers are:
            'XLooper': 1D looper (fallback).
            'XYLooper': 2D looper.
            'XYZLooper': 3D looper.
    file_path : str
        Path and prefix of the .npz file.
    plot: bool, optional
        Option to plot the results.
    width : float, optional
        Width of the figure.
    height : float, optional
        Height of the figure.

    Returns
    -------
    looper : :class:`qom.loopers.*`
        Instance of the looper.
    """
    
    # initialize logger
    init_log()

    # initialize system
    system = SystemClass(params['system'])

    # function to calculate average measure
    def func_measure_average(system_params, val, logger, results):
        # update parameters
        system.params = system_params
        # get dynamics
        M_avg = system.get_measure_average(params['solver'], system.ode_func, system.ivc_func)
        # update results
        results.append((val, M_avg))

    # function to calculate Pearson synchronization
    def func_measure_pearson(system_params, val, logger, results):
        # update parameters
        system.params = system_params
        # get dynamics
        m = system.get_measure_pearson(params['solver'], system.ode_func, system.ivc_func)
        # update results
        results.append((val, m))

    # function to calculate maximum eigenvalues of the drift matrix
    def func_TLE(system_params, val, logger, results):
        # update parameters
        system.params = system_params
        # get dynamics
        M = system.get_measure_dynamics(params['solver'], system.ode_func, system.ivc_func)
        # get modes
        modes = [np.mean([m[i] for m in M]) for i in range(len(M[0]))]
        # calculate eigenvalues
        eigs = system.get_eigenvalues_A(modes)[0]
        # update results
        results.append((val, np.max(np.real(eigs[6:]))))

    # select function
    if func_name == 'measure_pearson':
        func = func_measure_pearson
    elif func_name == 'TLE':
        func = func_TLE
    else:
        func = func_measure_average

    # select looper
    if looper_name == 'XYLooper':
        looper = XYLooper(func, params)
    elif looper_name == 'XYZLooper':
        looper = XYZLooper(func, params)
    else:
        looper = XLooper(func, params)
        
    # wrap looper
    looper.wrap(file_path, plot, width, height)

    return looper