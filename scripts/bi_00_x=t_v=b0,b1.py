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
from systems.Bi00 import Bi00

# all parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'cache_dir': 'H:/Workspace/data/bi_00/0.0_1000.0_10001',
        'method': 'ode',
        'measure_type': 'mode_amp',
        'idx_mode': [1, 3],
        'range_min': 0,
        'range_max': 10001,
        't_min': 0,
        't_max': 1000,
        't_dim': 10001
    },
    'system': {
        'A_l': 52.0,
        'Delta_0': 1.0, 
        'delta': 0.0, 
        'g_0s': [0.005, 0.005],
        'gammas': [0.005, 0.005],
        'kappas': [0.15, 0.15],
        'lamb': 0.075,
        'n_ths': [0, 0],
        'omega_m': 1.0
    },
    'plotter': {
        'type': 'lines',
        'palette': 'blr',
        'bins': 2,
        'x_label': '$\\omega_{mL} t$',
        'x_bound': 'both',
        'x_ticks': [490, 495, 500],
        'v_bound': 'both',
        'v_ticks': [-400, 0, 400],
        'show_legend': True,
        'legend_location': 'lower right', 
        'y_legend': ['$\\langle b_{L} \\rangle_{\\mathrm{Re}}$', '$\\langle b_{R} \\rangle_{\\mathrm{Re}}$'],
        'label_font_size': 44,
        'tick_font_size': 36
    }
}

# initialize log
init_log()

# initialize system
system = Bi00(params['system'])

# elements
M_ele, T = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)
M_ele = np.imag(M_ele)

# plotter
axes = {
    'X': T,
    'Y': {
        'var': 'b',
        'val': [0, 1]
    }
}
plotter = MPLPlotter(axes, params['plotter'])
_xs = [T, T]
_vs = np.transpose(M_ele).tolist()
plotter.update(xs=_xs, vs=_vs)
plotter.show(True, 7.5, 6.0)