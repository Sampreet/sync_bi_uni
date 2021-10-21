# dependencies
import itertools
import numpy as np
import os 
import sys

# qom modules
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems import Uni00

# parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'method': 'zvode',
        'measure_type': 'corr_ele',
        'idx_e': list(itertools.product([2, 3, 6, 7], [2, 3, 6, 7])),
        'range_min': 99371,
        'range_max': 100001,
        't_min': 0.0,
        't_max': 10000.0,
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
        'type': 'contourf',
        'title': '$\\delta = 0.005, \\eta = 0.75$',
        'x_label': '$\\langle p_{L} \\rangle$',
        'x_ticks': [-5, 0, 5],
        'y_label': '$\\langle p_{R} \\rangle$',
        'y_ticks': [-5, 0, 5],
        'cbar_title': '$\\times 10^{-4}$',
        'cbar_ticks': [0.0, 0.0004, 0.0008],
        'cbar_tick_labels': [0.0, 0.4, 0.8],
        'width': 5.5,
        'height': 5.0
    }
}

# initialize logger
init_log()

# initialize system
system = Uni00(params=params['system'])

# get correlation elements
M, _ = system.get_measure_dynamics(solver_params=params['solver'])
V_mech = [np.reshape(m, (4, 4)) for m in M[-1:]]

# initialize variables
q_0 = 0
q_1 = 0
p_0s = np.around(np.linspace(-5, 5, 101), 1)
p_1s = np.around(np.linspace(-5, 5, 101), 1)

for V in V_mech:
    # wigner function
    W = list()
    for p_0 in p_0s:
        temp = list()
        for p_1 in p_1s:
            X = np.array([q_0, p_0, q_1, p_1]).transpose()
            ele = np.exp(-1 / 2 * np.dot(X.transpose(), np.dot(np.linalg.inv(V), X))) / 4 / np.pi**2 / np.sqrt(np.linalg.det(V))
            temp.append(ele)
        W.append(temp)

    # plotter
    plotter = MPLPlotter(axes={
        'X': p_0s.tolist(),
        'Y': p_1s.tolist()
    }, params=params['plotter'])
    plotter.update(vs=W)
    plotter.show(True)