# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Uni02 import Uni02

# all parameters
params = {
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
        'type': 'lines',
        'palette': 'RdBu',
        'bins': 11,
        'x_label': '$\omega_{mL} t$',
        'x_bound': 'both',
        'x_ticks': [0, 25, 50, 75, 100],
        'v_label': '$S_{p}, 5 \\times D_{G}$',
        'label_font_size': 22,
        'tick_font_size': 18
    }
}

# initialize log
init_log()

# initialize system
system = Uni02(params['system'])

modes, corrs = system.get_modes_corrs_stationary(system.get_mode_rates, system.get_ivc, system.get_A)
print(modes, corrs)

# get correlation elements
M, T = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)
print(np.transpose(M))

# plotter
plotter = MPLPlotter({
    'X': T,
    'Y': {
        'var': 'QCM',
        'val': [0, 1]
    }
}, params['plotter'])
plotter.update(xs=[T, T], vs=np.transpose(M))
plotter.show(True, 8.0, 3.25)