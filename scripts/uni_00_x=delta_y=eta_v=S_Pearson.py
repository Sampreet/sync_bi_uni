# dependencies
import os 
import sys

# qom modules
from qom.utils.wrappers import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Uni00 import Uni00

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
        'cache': True,
        'cache_dir': 'H:/Workspace/VSCode/Python/sync_bi_uni/data/uni_00/0.0_10000.0_100001',
        'method': 'ode',
        'measure_type': 'corr_ele',
        'idx_row': [3, 3, 7],
        'idx_col': [3, 7, 7],
        'range_min': 99371,
        'range_max': 100001,
        't_min': 0,
        't_max': 10000,
        't_dim': 100001
    },
    'system': {
        'A_l': 52.0,
        'Delta_0': 1.0, 
        'delta': 0.005, 
        'eta': 0.75,
        'g_0s': [0.005, 0.005],
        'gammas': [0.005, 0.005],
        'kappas': [0.15, 0.15],
        'n_ths': [0, 0],
        'omega_m': 1.0
    },
    'plotter': {
        'type': 'contourf',
        'palette': 'RdBu_r',
        'bins': 11,
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_bound': 'both',
        'x_ticks': [0.0, 0.01, 0.02],
        'y_label': '$\\eta$',
        'y_bound': 'both',
        'y_ticks': [0.5, 0.75, 1.0],
        'cbar_title': '$C$',
        'cbar_ticks': [-1, 0, 1],
        'cbar_position': 'top',
        'label_font_size': 22,
        'tick_font_size': 18
    }
}

# get Pearson synchronization
looper = wrap_looper(Uni00, params, 'measure_average', 'XYLooper', 'H:/Workspace/VSCode/Python/sync_bi_uni/data/uni_00/S_Pearson_1e4-20pi', True)
print(looper.get_thresholds(thres_mode='minmax'))