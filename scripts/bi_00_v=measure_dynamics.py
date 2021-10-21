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
from systems import Bi00

# parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'method': 'zvode',
        'measure_type': 'sync_p',
        'idx_e': (1, 3),
        'range_min': 0,
        'range_max': 10001,
        't_min': 0.0,
        't_max': 1000.0,
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
        'x_label': '$\\omega_{mL} t$',
        'x_ticks': [0, 200, 400, 600],
        'v_label': '$S_{p}, 5 \\times D_{G}$',
        'v_ticks': [0, 0.1, 0.2],
        'width': 8.0,
        'height': 4.0
    }
}

# initialize logger
init_log()

# initialize system
system = Bi00(params=params['system'])

# get phase synchronization
params['solver']['measure_type'] = 'sync_p'
M_0, T = system.get_measure_dynamics(solver_params=params['solver'])
M_0_avg = np.mean(M_0[9371:])

# get Gaussian discord
params['solver']['measure_type'] = 'discord_G'
M_1, T = system.get_measure_dynamics(solver_params=params['solver'])
M_1 = [5 * m for m in M_1]
M_1_avg = np.mean(M_1[9371:])

# plotter
plotter = MPLPlotter(axes={
    'X': T,
    'Y': ['$S_{p}$', '$5 \\times D_{G}$']
}, params=params['plotter'])
_colors = plotter.get_colors(palette=params['plotter']['palette'], bins=params['plotter']['bins'])
axis = plotter.get_current_axis()
axis.plot([M_0_avg for i in range(len(T))], linestyle='--', color=_colors[-2])
axis.plot([M_1_avg for i in range(len(T))], linestyle='--', color=_colors[1])
axis.plot(T, M_0, color=_colors[-2])
axis.plot(T, M_1, color=_colors[1])
plotter.show(hold=True)