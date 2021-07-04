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
        'cache_dir': 'H:/Workspace/VSCode/Python/sync_bi_uni/data/bi_00/0.0_1000.0_10001',
        'method': 'ode',
        'measure_type': 'corr_ele',
        'idx_row': [2, 2, 2, 2, 3, 3, 3, 3, 6, 6, 6, 6, 7, 7, 7, 7],
        'idx_col': [2, 3, 6, 7, 2, 3, 6, 7, 2, 3, 6, 7, 2, 3, 6, 7],
        'range_min': 9371,
        'range_max': 10001,
        't_min': 0,
        't_max': 1000,
        't_dim': 10001
    },
    'system': {
        'A_l': 52.0,
        'Delta_0': 1.0, 
        'delta': 0.0116, 
        'g_0s': [0.005, 0.005],
        'gammas': [0.005, 0.005],
        'kappas': [0.15, 0.15],
        'lamb': 0.05,
        'n_ths': [0, 0],
        'omega_m': 1.0
    },
    'plotter': {
        'type': 'contourf',
        'palette': 'RdBu_r',
        'bins': 11,
        'title': '$\\delta = 0.0116, \\lambda = 0.05$',
        'x_label': '$\\langle q_{R} \\rangle$',
        'x_bound': 'both',
        'x_ticks': [-20, 0, 20],
        'y_label': '$\\langle p_{R} \\rangle$',
        'y_bound': 'both',
        'y_ticks': [-20, 0, 20],
        'cbar_ticks': [0, 0.0005],
        'label_font_size': 33,
        'tick_font_size': 27
    }
}

# initialize logger
init_log()

# initialize system
system = Bi00(params['system'])

# get dynamics
M, _ = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)
V_mech = [np.reshape(m, (4, 4)) for m in M[-1:]]

# initialize variables
q_0 = 0
p_0 = 0
q_1s = np.around(np.linspace(-20, 20, 101), 1)
p_1s = np.around(np.linspace(-20, 20, 101), 1)

for V in V_mech:
    # wigner
    W = list()
    for q_1 in q_1s:
        temp = list()
        for p_1 in p_1s:
            X = np.array([q_0, p_0, q_1, p_1])
            ele = np.exp(-1 / 2 * np.dot(X, np.dot(np.linalg.inv(V), np.transpose(X)))) / 4 / np.pi**2 / np.sqrt(np.linalg.det(V))
            temp.append(ele)
        W.append(temp)

    # plotter
    axes = {
        'X': q_1s.tolist(),
        'Y': p_1s.tolist()
    }
    plotter = MPLPlotter(axes, params['plotter'])
    plotter.update(vs=W)
    plotter.show(True, 6.0, 5.0)