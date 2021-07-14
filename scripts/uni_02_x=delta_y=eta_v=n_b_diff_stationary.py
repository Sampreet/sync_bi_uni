# dependencies
import os 
import sys

# qom modules
from qom.utils.wrappers import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Uni02 import Uni02

# all parameters
params = {
    'looper': {
        'mode': 'multithread',
        'X': {
            'var': 'delta',
            'min': 0.0,
            'max': 0.02,
            'dim': 101
        },
        'Y': {
            'var': 'eta',
            'min': 0.5,
            'max': 1.0,
            'dim': 101
        }
    },
    'system': {
        'A_l': 52.0,
        'Delta_0': 1.0, 
        'delta': 0.0,
        'eta': 0.75,
        'g_0s': [0.005, 0.005],
        'gammas': [0.005, 0.005],
        'kappas': [0.15, 0.15],
        'n_ths': [0, 0],
        'omega_m': 1.0
    },
    'plotter': {
        'type': 'contourf',
        'palette': 'blr',
        'bins': 11,
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_bound': 'both',
        'x_ticks': [0.0, 0.01, 0.02],
        'y_label': '$\\eta$',
        'y_bound': 'both',
        'y_ticks': [0.5, 0.75, 1.0],
        'cbar_title': '$n_{b_{R}} - n_{b_{L}}$',
        'cbar_ticks': [- 0.2, - 0.1, 0.0],
        'cbar_position': 'top',
        'label_font_size': 22,
        'tick_font_size': 18
    }
}

# function to obtain the difference between the phonon numbers
def func_n_b_diff(system_params, val, logger, results):
    # update system
    system = Uni02(system_params)
    # # get difference
    # n_b_diff = system.get_n_b_diff()
    # get steady state values
    _, corrs = system.get_modes_corrs_stationary(system.get_mode_rates, system.get_ivc, system.get_A)
    # difference
    n_b_diff = (corrs[3][3] + corrs[2][2] - corrs[1][1] - corrs[0][0]) / 2
    # update results
    results.append((val, n_b_diff))

# looper 
looper = wrap_looper(Uni02, params, func_n_b_diff, 'XYLooper', plot=True)