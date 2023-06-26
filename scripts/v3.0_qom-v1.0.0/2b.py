# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.solvers import HLESolver, QCMSolver
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('.')))
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
        'type'                  : 'lines',
        'x_label'               : '$\\omega_{mL} t$',
        'x_tick_position'       : 'both-out',
        'x_ticks'               : [0, 200, 400, 600],
        'x_ticks_minor'         : [i * 40 for i in range(16)],
        'y_colors'              : [0, 0, -1, -1],
        'y_styles'              : ['-', '--'] * 2,
        'v_label'               : '$S_{p}$',
        'v_label_color'         : 0,
        'v_tick_position'       : 'both-out',
        'v_ticks'               : [0, 0.1, 0.2],
        'v_ticks_minor'         : [i * 0.02 for i in range(11)],
        'v_twin_label'          : '$5 \\times D_{G}$',
        'v_twin_label_color'    : -1,
        'v_twin_tick_position'  : 'both-out',
        'v_twin_ticks'          : [0, 0.1, 0.2],
        'v_twin_ticks_minor'    : [i * 0.02 for i in range(11)],
        'width'                 : 8.0,
        'height'                : 4.0
    }
}

# initialize logger
init_log()

# initialize system
system = Uni_00(
    params=params['system']
)

# get modes, correlations and times
Modes, Corrs, T = HLESolver(
    system=system,
    params=params['solver']
).get_modes_corrs_times()
# get quantum correlation measures
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
plotter = MPLPlotter(
    axes={},
    params=params['plotter']
)
plotter.update(
    xs=T,
    vs=[M_0, [M_0_avg] * len(T)]
)
plotter.update_twin_axis(
    xs=T,
    vs=[M_1, [M_1_avg] * len(T)]
)
plotter.show(
    hold=True
)