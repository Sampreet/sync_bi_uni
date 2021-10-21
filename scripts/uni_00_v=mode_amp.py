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
from systems import Uni00

# all parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'method': 'zvode',
        'measure_type': 'mode_amp',
        'idx_e': [1, 3],
        'range_min': 9900,
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
        'x_label': '$\\omega_{mL} t$',
        'x_ticks': [990, 995, 1000],
        'v_ticks': [-400, 0, 400],
        'show_legend': True,
        'legend_location': 'upper right', 
        'label_font_size': 44,
        'tick_font_size': 36,
        'width': 7.5,
        'height': 6.0
    }
}

# initialize log
init_log()

# initialize system
system = Uni00(params=params['system'])

# get mode amplitudes
M, T = system.get_measure_dynamics(solver_params=params['solver'])
M_real = np.real(M)

# plotter
plotter = MPLPlotter(axes={
    'X': T,
    'Y': ['$\\langle b_{L} \\rangle_{\\mathrm{Re}}$', '$\\langle b_{R} \\rangle_{\\mathrm{Re}}$']
}, params=params['plotter'])
plotter.update(xs=T, vs=np.transpose(M_real))
plotter.show(True)