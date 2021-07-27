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
        'cache_dir': 'H:/Workspace/data/uni_00/0.0_10000.0_100001',
        'method': 'ode',
        'measure_type': 'qcm',
        'qcm_type': 'sync_phase',
        'idx_mode_i': 1,
        'idx_mode_j': 3,
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
        'palette': 'Blues',
        'bins': 11,
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_bound': 'both',
        'x_ticks': [0.0, 0.01, 0.02],
        'y_label': '$\\eta$',
        'y_bound': 'both',
        'y_ticks': [0.5, 0.75, 1.0],
        'cbar_ticks': [0.0, 0.04, 0.08],
        'cbar_title': '$\\langle S_{p} \\rangle$',
        'cbar_ticks': [0.0, 0.1, 0.2],
        'cbar_position': 'top',
        'label_font_size': 22,
        'tick_font_size': 18
    }
}

# get average phase synchronization
looper = wrap_looper(Uni00, params, 'measure_average', 'XYLooper', 'H:/Workspace/data/uni_00/S_phase_avg_1e4-20pi', True)
print(looper.get_thresholds(thres_mode='minmax'))