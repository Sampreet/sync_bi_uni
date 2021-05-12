# dependencies
import os 
import sys

# qom modules
from qom.loopers import XLooper
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Bi00 import Bi00

# all parameters
params = {
    'looper': {
        'show_progress': True,
        'X': {
            'var': 'delta',
            'min': -0.02,
            'max': 0.02,
            'dim': 11
        }
    },
    'solver': {
        'cache': True,
        'cache_dir': 'H:/Workspace/VSCode/Python/sync_bi_uni/data/bi_00/0.0_1000.0_10001',
        'method': 'ode',
        'range_min': 9371,
        'range_max': 10001,
        't_min': 0,
        't_max': 1000,
        't_dim': 10001
    },
    'system': {
        'A_l': 52.0,
        'Delta_0': 1.0, 
        'delta': 0.005, 
        'g_0s': [0.005, 0.005],
        'gammas': [0.005, 0.005],
        'kappas': [0.15, 0.15],
        'lamb': 0.075,
        'n_ths': [0, 0],
        'omega_m': 1.0
    },
    'plotter': {
        'type': 'lines',
        'palette': 'Blues',
        'bins': 3,
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_bound': 'both',
        'x_ticks': [-0.02, -0.01, 0.0, 0.01, 0.02],
        'v_label': '$\\langle S_{p} \\rangle, 20 \\times \\langle D_{G} \\rangle, C$',
        'v_bound': 'both',
        'v_ticks': [-1.0, -0.5, 0.0, 0.5, 1.0],
    }
}

# initialize log
init_log()

# initialize system
system = Bi00(params['system'])

# function to calculate average measure
def func_measure_average(system_params, val, logger, results):
    # update parameters
    system.params = system_params
    # get dynamics
    M_avg = system.get_measure_average(params['solver'], system.ode_func, system.ivc_func)
    # update results
    results.append((val, M_avg))

# get average phase synchronization
params['solver']['measure_type'] = 'qcm'
params['solver']['qcm_type'] = 'sync_phase'
params['solver']['idx_mode_i'] = 1
params['solver']['idx_mode_j'] = 3
looper = XLooper(func_measure_average, params)
looper.loop()
S_phase_avg = looper.results['V']

# get average Gaussian discord
params['solver']['measure_type'] = 'qcm'
params['solver']['qcm_type'] = 'discord'
params['solver']['idx_mode_i'] = 1
params['solver']['idx_mode_j'] = 3
looper = XLooper(func_measure_average, params)
looper.loop()
D_G_avg = looper.results['V']

# function to calculate Pearson synchronization measure
def func_measure_pearson(system_params, val, logger, results):
    # update parameters
    system.params = system_params
    # get dynamics
    S_Pearson = system.get_measure_pearson(params['solver'], system.ode_func, system.ivc_func)
    # update results
    results.append((val, S_Pearson))

# get Pearson synchronization
params['solver']['measure_type'] = 'corr_ele'
params['solver']['idx_row'] = [3, 3, 7]
params['solver']['idx_col'] = [3, 7, 7]
looper = XLooper(func_measure_pearson, params)
looper.loop()
S_Pearson = looper.results['V']

# plotter
X = looper.axes['X']['val']
axes = {
    'X': X,
    'Y': {
        'var': 'QCM',
        'val': [0, 1, 2]
    }
}
plotter = MPLPlotter(axes, params['plotter'])
_xs = [X, X, X]
_vs = [S_phase_avg, [20 * m for m in D_G_avg], S_Pearson]
plotter.update(xs=_xs, vs=_vs)
plotter.show(True, 6.0, 5.0)