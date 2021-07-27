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
from systems.Uni00 import Uni00

# all parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'cache_dir': 'H:/Workspace/data/uni_00/0.0_10000.0_100001',
        'method': 'ode',
        'measure_type': 'corr_ele',
        'idx_row': [3, 7],
        'idx_col': [3, 7],
        'range_min': 9371,
        'range_max': 10001,
        't_min': 0,
        't_max': 10000,
        't_dim': 100001
    },
    'system': {
        'A_l': 52.0,
        'Delta_0': 1.0, 
        'delta': 0.01, 
        'eta': 0.75,
        'g_0s': [0.005, 0.005],
        'gammas': [0.005, 0.005],
        'kappas': [0.15, 0.15],
        'n_ths': [0, 0],
        'omega_m': 1.0
    },
    'plotter': {
        'type': 'lines',
        'palette': 'blr',
        'bins': 2,
        'x_label': '$\\omega_{mL} t$',
        'x_bound': 'both',
        'x_ticks': [990, 995, 1000],
        'v_bound': 'both',
        'v_ticks': [0, 400, 800],
        'show_legend': True,
        'legend_location': 'lower right', 
        'y_legend': ['$\\langle \\delta p_{L}^{2} \\rangle$', '$\\langle \\delta p_{R}^{2} \\rangle$'],
        'label_font_size': 44,
        'tick_font_size': 36
    }
}

# initialize log
init_log()

# initialize system
system = Uni00(params['system'])

# elements
M_ele, T = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)
M_ele = np.real(M_ele)

# plotter
axes = {
    'X': T,
    'Y': {
        'var': 'delta_p',
        'val': [0, 1]
    }
}
plotter = MPLPlotter(axes, params['plotter'])
_xs = [T, T]
_vs = np.transpose(M_ele)
plotter.update(xs=_xs, vs=_vs)
plotter.show(True, 7.5, 6.0)