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

# parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'cache_dir': 'H:/Workspace/data/bi_00/0.0_1000.0_10001',
        'method': 'ode',
        'measure_type': 'qcm',
        'qcm_type': 'sync_phase',
        'idx_mode_i': 1,
        'idx_mode_j': 3,
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
        'palette': 'RdBu',
        'bins': 11,
        'x_label': '$t / \\tau$',
        'x_bound': 'both',
        'x_ticks': [0, 200, 400, 600],
        'v_label': '$S_{p}, 5 \\times D_{G}$',
        'v_bound': 'both',
        'v_ticks': [0, 0.1, 0.2],
        'label_font_size': 22,
        'tick_font_size': 18
    }
}

# initialize logger
init_log()

# initialize system
system = Bi00(params['system'])

# get phase synchronization
params['solver']['qcm_type'] = 'sync_phase'
M_sync, T = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)
sync_avg = np.mean(M_sync[9371:])

# get Gaussian discord
params['solver']['qcm_type'] = 'discord'
M_disc, T = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)
disc_avg = np.mean(M_disc[9371:])

# plotter
axes = {
    'X': T,
    'Y': {
        'var': 'QCM',
        'val': [0, 1]
    }
}
plotter = MPLPlotter(axes, params['plotter'])
_colors = plotter.axes['Y'].colors
plotter.get_current_axis().plot([sync_avg for i in range(len(T))], linestyle='--', color=_colors[-2])
plotter.get_current_axis().plot([5 * disc_avg for i in range(len(T))], linestyle='--', color=_colors[1])
_xs = [T, T]
_vs = [M_sync, [5 * m for m in M_disc]]
plotter.get_current_axis().plot(_xs[0], _vs[0], color=_colors[-2])
plotter.get_current_axis().plot(_xs[1], _vs[1], color=_colors[1])
plotter.show(True, 8.0, 4.0)