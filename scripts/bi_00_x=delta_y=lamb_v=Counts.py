# dependencies
import os 
import sys

# qom modules
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Bi00 import Bi00
# import counter
from utils.counters import count_pixels

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
        'measure_type': 'mode_amp',
        'idx_mode': 2,
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
        'type': 'line',
        'palette': 'blr',
        'bins': 2,
        'x_bound': 'both',
        'x_ticks': [-100, 0, 100],
        'x_tick_labels': ['', '', ''],
        'v_bound': 'both',
        'v_ticks': [-100, 0, 100],
        'v_tick_labels': ['', '', ''],
        'label_font_size': 44,
        'tick_font_size': 36
    }
}

# get counts
Counts = count_pixels(Bi00, params, 'H:/Workspace/VSCode/Python/sync_bi_uni/data/bi_00/Counts_1e3-20pi', 'H:/Workspace/VSCode/Python/sync_bi_uni/img/bi_00/0.0_1000.0_10001/a1', 4, 3)

# plotter
plotter = MPLPlotter({
    'X': params['looper']['X'],
    'Y': params['looper']['Y']
}, {
    'type': 'pcolormesh',
    'palette': 'RdBu_r',
    'bins': 11,
    'x_label': '$\\delta / \\omega_{mL}$',
    'x_bound': 'both',
    'x_ticks': [-0.02, 0.0, 0.02],
    'y_label': '$\\lambda / \\omega_{mL}$',
    'y_bound': 'both',
    'y_ticks': [0.0, 0.04, 0.08],
    'show_cbar': False,
    'label_font_size': 22,
    'tick_font_size': 18
})
plotter.update(vs=Counts)
plotter.show(True)