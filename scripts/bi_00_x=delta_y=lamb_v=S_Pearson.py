# dependencies
import os 
import sys

# qom modules
from qom.utils.wrappers import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Bi00 import Bi00

# all parameters
params = {
    'looper': {
        'X': {
            'var': 'delta',
            'min': -0.02,
            'max': 0.02,
            'dim': 101
        },
        'Y': {
            'var': 'lamb',
            'min': 0.0,
            'max': 0.1,
            'dim': 101
        }
    },
    'solver': {
        'cache': True,
        'cache_dir': 'H:/Workspace/VSCode/Python/sync_bi_uni/data/bi_00/0.0_1000.0_10001',
        'method': 'ode',
        'measure_type': 'corr_ele',
        'idx_row': [3, 3, 7],
        'idx_col': [3, 7, 7],
        'range_min': 9371,
        'range_max': 10001,
        't_min': 0,
        't_max': 1000,
        't_dim': 10001
    },
    'system': {
        'A_l': 52.0,
        'Delta_0': 1.0, 
        'delta': 0.005, 
        'g_0s': [0.005, 0.005],
        'gammas': [0.005, 0.005],
        'kappas': [0.15, 0.15],
        'lamb': 0.075,
        'n_ths': [0, 0],
        'omega_m': 1.0
    },
    'plotter': {
        'type': 'contourf',
        'palette': 'Blues',
        'bins': 11,
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_bound': 'both',
        'x_ticks': [-0.02, 0.0, 0.02],
        'y_label': '$\\lambda / \\omega_{mL}$',
        'y_bound': 'both',
        'y_ticks': [0.0, 0.04, 0.08],
        'cbar_title': '$C$',
        'cbar_ticks': [0.0, 0.5, 1.0],
        'cbar_position': 'top',
        'label_font_size': 22,
        'tick_font_size': 18
    }
}

# get Pearson synchronization
looper = wrap_looper(Bi00, params, 'measure_pearsonn', 'XYLooper', 'H:/Workspace/VSCode/Python/sync_bi_uni/data/bi_00/S_Pearson_1e3-20pi', True)
print(looper.get_thresholds(thres_mode='minmax'))