# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.utils.loopers import run_loopers_in_parallel, wrap_looper
from qom.utils.solvers import get_func_quantum_correlation_measures

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('.')))
# import system
from systems.Unidirectional import Uni_00

# all parameters
params = {
    'looper': {
        'show_progress'     : True,
        'file_path_prefix'  : 'data/v3.0_qom-v1.0.1/4b',
        'X'                 : {
            'var'   : 'delta',
            'min'   : 0.00,
            'max'   : 0.02,
            'dim'   : 101
        },
        'Y'                 : {
            'var'   : 'eta',
            'min'   : 0.5,
            'max'   : 1.0,
            'dim'   : 101
        }
    },
    'solver': {
        'show_progress' : False,
        'cache'         : True,
        'measure_codes' : ['sync_p'],
        'indices'       : [1, 3],
        'ode_method'    : 'vode',
        't_min'         : 0.0,
        't_max'         : 10000.0,
        't_dim'         : 100001,
        't_index_min'   : 99371,
        't_index_max'   : 100000
    },
    'system': {
        'A_l'           : 52.0,
        'Delta_0_sign'  : 1.0, 
        'delta'         : 0.01,
        'eta'           : 0.75,
        'g_0s'          : [0.005, 0.005],
        'gammas'        : [0.005, 0.005],
        'kappas'        : [0.15, 0.15],
        'n_ths'         : [0.0, 0.0],
        'omega_mL'      : 1.0
    },
    'plotter': {
        'type'              : 'contourf',
        'x_label'           : '$\\delta / \\omega_{mL}$',
        'x_tick_position'   : 'both-out',
        'x_ticks'           : [0.0, 0.01, 0.02],
        'x_ticks_minor'     : [i * 0.002 for i in range(11)],
        'y_label'           : '$\\eta$',
        'y_tick_position'   : 'both-out',
        'y_ticks'           : [0.5, 0.75, 1.0],
        'y_ticks_minor'     : [i * 0.05 + 0.5 for i in range(11)],
        'show_cbar'         : True,
        'cbar_title'        : '$\\langle S_{p} \\rangle$',
        'cbar_ticks'        : [0.0, 0.1, 0.2],
        'width'             : 5.5
    }
}

# function to obtain quantum phase synchronization
def func(system_params):
    # get quantum correlation measures
    Measures = get_func_quantum_correlation_measures(
        SystemClass=Uni_00,
        params=params['solver'],
        steady_state=False
    )(system_params)
    # return average value
    return np.mean(Measures.transpose()[0])

# loop and plot
if __name__ == '__main__':
    looper = run_loopers_in_parallel(
        looper_name='XYLooper',
        func=func,
        params=params['looper'],
        params_system=params['system'],
        plot=True,
        params_plotter=params['plotter']
    )