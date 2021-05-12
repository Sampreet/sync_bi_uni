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
        'cache_dir': 'H:/Workspace/VSCode/Python/sync_bi_uni/data/bi_00/0.0_1000.0_10001',
        'method': 'ode',
        'measure_type': 'corr_ele',
        'idx_row': [3, 7],
        'idx_col': [3, 7],
        'range_min': 0,
        'range_max': 10001,
        't_min': 0,
        't_max': 1000,
        't_dim': 10001
    },
    'system': {
        'A_l': 52.0,
        'Delta_0': 1.0, 
        'delta': 0.01, 
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
        'v_ticks': [0, 100, 200],
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
system = Bi00(params['system'])

# elements
M_ele = system.get_measure_dynamics(params['solver'], system.ode_func, system.ivc_func)
M_ele = np.real(M_ele)

# plotter
t_min = params['solver']['range_min']
t_max = params['solver']['range_max']
t_ss = (params['solver']['t_dim'] - 1) / params['solver']['t_max']
T = np.linspace(t_min / t_ss, t_max / t_ss, t_max - t_min).tolist()
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