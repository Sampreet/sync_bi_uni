# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.ui import init_log
from qom.loopers import XYLooper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Uni02 import Uni02

# all parameters
params = {
    'looper': {
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
    'solver': {
        'show_progress': True,
        'cache': False,
        'cache_dir': 'H:/Workspace/VSCode/Python/sync_bi_uni/data/uni_02/0.0_10000.0_100001',
        'method': 'RK45',
        'measure_type': 'corr_ele',
        'idx_row': [0, 1, 2, 3],
        'idx_col': [0, 1, 2, 3],
        'range_min': 0,
        'range_max': 1001,
        't_min': 0,
        't_max': 100,
        't_dim': 1001
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
        'palette': 'Reds',
        'bins': 11,
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_bound': 'both',
        'x_ticks': [0.0, 0.01, 0.02],
        'y_label': '$\\eta$',
        'y_bound': 'both',
        'y_ticks': [0.5, 0.75, 1.0],
        'cbar_title': '$n_{n_{2}} - n_{n_{1}}$',
        'cbar_ticks': [- 0.007119, - 0.007117, - 0.007115],
        'cbar_position': 'top',
        'label_font_size': 22,
        'tick_font_size': 18
    }
}

# initialize system
system = Uni02(params['system'])

# get steady state values
modes, corrs = system.get_modes_corrs_stationary(system.get_mode_rates, system.get_ivc, system.get_A)
# difference
print((corrs[3][3] + corrs[2][2] - corrs[1][1] - corrs[0][0]) / 2)

# initialize log
init_log()

# initialize system
system = Uni02(params['system'])

# function to obtain the difference between the phonon numbers
def func_n_b_diff(system_params, val, logger, results):
    # update system
    system.params = system_params
    # get difference
    n_b_diff = system.get_n_b_diff()
    # update results
    results.append((val, n_b_diff))

# looper 
looper = XYLooper(func_n_b_diff, params)
looper.loop(plot=True)