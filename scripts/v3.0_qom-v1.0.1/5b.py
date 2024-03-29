# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.ui.plotters import MPLPlotter
from qom.utils.loopers import run_loopers_in_parallel, wrap_looper
from qom.utils.solvers import get_func_quantum_correlation_measures, get_func_system_measures

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('.')))
# import system
from systems.Unidirectional import Uni_00, Uni_01

# all parameters
params = {
    'looper': {
        'show_progress'     : True,
        'file_path_prefix'  : 'data/v3.0_qom-v1.0.1/5b',
        'X'                 : {
            'var'   : 'delta',
            'min'   : 0.00,
            'max'   : 0.01,
            'dim'   : 51
        }
    },
    'solver': {
        'show_progress'         : False,
        'cache'                 : True,
        'measure_codes'         : ['sync_p'],
        'system_measure_name'   : 'A',
        'indices'               : [1, 3],
        'ode_method'            : 'vode',
        't_min'                 : 0.0,
        't_max'                 : 10000.0,
        't_dim'                 : 100001,
        't_index_min'           : 99371,
        't_index_max'           : 100000
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
        'colors'                : [-1, 'k', 'k'],
        'styles'                : ['-', ':', '--'],
        'x_label'               : '$\\delta / \\omega_{mL}$',
        'x_tick_position'       : 'both-out',
        'x_ticks'               : [i * 0.002 for i in range(6)],
        'x_ticks_minor'         : [i * 0.0004 for i in range(26)],
        'v_label'               : '$10^{3} \\times TLE$',
        'v_label_color'         : -1,
        'v_tick_color'          : -1,
        'v_limits'              : [-0.0015, 0.0005],
        'v_tick_labels'         : [-1, 0],
        'v_tick_position'       : 'both-out',
        'v_ticks'               : [-0.001, 0.0],
        'v_ticks_minor'         : [i * 0.0005 - 0.0015 for i in range(9)],
        'v_twin_label'          : '$\\langle S_{p} \\rangle$',
        'v_twin_ticks'          : [0.00, 0.08, 0.16],
        'v_twin_tick_position'  : 'both-out',
        'v_twin_ticks_minor'    : [i * 0.02 for i in range(9)],
        'width'                 : 8.0,
        'height'                : 4.0,
        'vertical_spans'        : [
            {
                'limits': (0.0, 0.0023),
                'color' : 5,
                'alpha' : 0.5
            },
            {
                'limits': (0.0023, 0.0033),
                'color' : -2,
                'alpha' : 0.5
            },
            {
                'limits': (0.0033, 0.0039),
                'color' : 5,
                'alpha' : 0.5
            },
            {
                'limits': (0.0039, 0.01),
                'color' : -4,
                'alpha' : 0.5
            }
        ]
    }
}

# function to obtain quantum phase synchronization and largest transverse Lyapunov exponent
def func(system_params):
    # get quantum correlation measures
    S_ps = get_func_quantum_correlation_measures(
        SystemClass=Uni_00,
        params=params['solver'],
        steady_state=False
    )(system_params)
    # return results
    m_00 = np.mean(S_ps, axis=0)[0]

    # get system measure
    As = get_func_system_measures(
        SystemClass=Uni_01,
        params=params['solver'],
        steady_state=False
    )(system_params)
    # get eigenvalues of the minus mode
    eigs, _ = np.linalg.eig(np.mean(As, axis=0))
    m_01 = np.max(np.real(eigs[6:8]))

    return np.array([m_00, m_01])

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
    vs = np.transpose(looper.results['V'])

    # plotter
    plotter = MPLPlotter(
        axes={},
        params=params['plotter']
    )
    plotter.update(
        vs=[vs[1], [0] * len(vs[1])],
        xs=xs
    )
    plotter.add_scatter(
        vs=vs[1],
        xs=xs,
        color=params['plotter']['colors'][0],
        size=20,
        style='o'
    )
    plotter.update_twin_axis(
        vs=vs[0],
        xs=xs
    )
    plotter.show()