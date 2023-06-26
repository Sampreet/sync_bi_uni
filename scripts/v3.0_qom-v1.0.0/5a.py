# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.ui.plotters import MPLPlotter
from qom.utils.looper import run_loopers_in_parallel, wrap_looper
from qom.utils.solver import get_func_quantum_correlation_measures

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('.')))
# import system
from systems.Unidirectional import Uni_00

# all parameters
params = {
    'looper': {
        'show_progress'     : True,
        'file_path_prefix'  :'data/v3.0_qom-v1.0.0/5a',
        'X' : {
            'var'   : 'delta',
            'min'   : 0.00,
            'max'   : 0.01,
            'dim'   : 51
        }
    },
    'solver': {
        'show_progress' : False,
        'cache'         : True,
        'measure_codes' : ['sync_p', 'corrs_P_p'],
        'indices'       : [1, 3],
        'method'        : 'vode',
        't_min'         : 0.0,
        't_max'         : 10000.0,
        't_dim'         : 100001,
        't_range_min'   : 99371,
        't_range_max'   : 100000
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
        'type'                  : 'lines',
        'x_label'               : '$\\delta / \\omega_{mL}$',
        'x_tick_position'       : 'both-out',
        'x_ticks'               : [i * 0.002 for i in range(6)],
        'x_ticks_minor'         : [i * 0.0004 for i in range(26)],
        'y_colors'              : [0, 'k', 'k'],
        'y_styles'              : ['-', ':', '--'],
        'v_label'               : '$C$',
        'v_label_color'         : 0,
        'v_tick_position'       : 'both-out',
        'v_ticks'               : [-1, 0, 1],
        'v_ticks_minor'         : [i * 0.25 - 1.0 for i in range(9)],
        'v_twin_label'          : '$\\langle S_{p} \\rangle$',
        'v_twin_ticks'          : [0.00, 0.08, 0.16],
        'v_twin_tick_position'  : 'both-out',
        'v_twin_ticks_minor'    : [i * 0.02 for i in range(9)],
        'width'                 : 8.0,
        'height'                : 4.0,
        'vspan'                 : [
            {
                'xmin'  : 0.0,
                'xmax'  : 0.0023,
                'color' : 5,
                'alpha' : 0.5
            },
            {
                'xmin'  : 0.0023,
                'xmax'  : 0.0033,
                'color' : 2,
                'alpha' : 0.5
            },
            {
                'xmin'  : 0.0033,
                'xmax'  : 0.0039,
                'color' : 5,
                'alpha' : 0.5
            },
            {
                'xmin'  : 0.0039,
                'xmax'  : 0.01,
                'color' : 4,
                'alpha' : 0.5
            }
        ]
    }
}

# function to obtain quantum phase synchronization and pearson correlation coefficient
def func(system_params):
    # get quantum correlation measures
    Measures = get_func_quantum_correlation_measures(
        SystemClass=Uni_00,
        params=params['solver'],
        steady_state=False
    )(system_params)
    # return average value
    return np.mean(Measures, axis=0)

if __name__ == '__main__':
    # looper
    looper = run_loopers_in_parallel(
        looper_name='XLooper',
        func=func,
        params=params['looper'],
        params_system=params['system'],
        plot=False
    )

    # extract values
    xs = looper.axes['X']['val']
    vs = looper.results['V'].transpose()

    # plotter
    plotter = MPLPlotter(
        axes={
            'X' : xs,
            'Y' : ['sync_p', 'corr_P']
        },
        params=params['plotter']
    )
    plotter.update(
        xs=xs,
        vs=[vs[1], [0] * len(vs[1])]
    )
    plotter.add_scatter(
        xs=xs,
        vs=vs[1],
        size=20,
        color=params['plotter']['y_colors'][0],
        marker='o'
    )
    plotter.update_twin_axis(
        xs=xs,
        vs=vs[0]
    )
    plotter.show(
        hold=True
    )