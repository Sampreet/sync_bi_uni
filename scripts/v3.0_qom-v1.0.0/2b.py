# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.solvers import HLESolver, QCMSolver
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Unidirectional import Uni_00

# parameters
params = {
    'solver': {
        'show_progress' : True,
        'cache'         : False,
        'measure_codes' : ['sync_p', 'discord_G'],
        'indices'       : [1, 3],
        'method'        : 'vode',
        't_min'         : 0.0,
        't_max'         : 1000.0,
        't_dim'         : 10001,
        't_range_min'   : 0,
        't_range_max'   : 10000,
    },
    'system': {
        'A_l'           : 52.0,
        'Delta_0_sign'  : 1.0, 
        'delta'         : 0.01,
        'eta'           : 0.75,
        'g_0s'          : [0.005, 0.005],
        'gammas'        : [0.005, 0.005],
        'kappas'        : [0.15, 0.15],
        'n_ths'         : [0.0, 0.0],
        'omega_mL'      : 1.0
    },
    'plotter': {
        'type'              : 'lines',
        'palette'           : 'RdBu',
        'bins'              : 11,
        'x_label'           : '$\\omega_{mL} t$',
        'x_tick_position'   : 'both-out',
        'x_ticks'           : [0, 200, 400, 600],
        'x_ticks_minor'     : [i * 40 for i in range(16)],
        'v_label'           : '$S_{p}, 5 \\times D_{G}$',
        'v_tick_position'   : 'both-out',
        'v_ticks'           : [0, 0.1, 0.2],
        'v_ticks_minor'     : [i * 0.02 for i in range(11)],
        'width'             : 8.0,
        'height'            : 4.0
    }
}

# initialize logger
init_log()

# initialize system
system = Uni_00(
    params=params['system']
)

# get modes and correlations
Modes, Corrs, T = HLESolver(
    system=system,
    params=params['solver']
).get_modes_corrs_dynamics()
# get measures
Measures = QCMSolver(
    Modes=Modes,
    Corrs=Corrs,
    params=params['solver']
).get_measures()

# extract required values
M_0 = Measures.transpose()[0]
M_0_avg = np.mean(M_0[9371:])
M_1 = Measures.transpose()[1] * 5
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