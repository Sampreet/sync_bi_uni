# dependencies
import os 
import sys

# qom modules
from qom.ui.plotters import MPLPlotter
from qom.utils.looper import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems import Bi00

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
        'method': 'zvode',
        'range_min': 9371,
        'range_max': 10001,
        't_min': 0.0,
        't_max': 1000.0,
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
        'x_ticks': [-0.02, -0.01, 0.0, 0.01, 0.02],
        'v_ticks': [-0.5, 0.0, 0.5, 1.0],
        'show_legend': True,
        'legend_location': 'upper right',
        'width': 8.0,
        'height': 4.0
    }
}

# get average phase synchronization
params['solver']['measure_type'] = 'sync_p'
params['solver']['idx_e'] = (1, 3)
looper = wrap_looper(SystemClass=Bi00, params=params, func='mav', looper='x_looper', file_path='data/bi_00/sync_p_avg_1e3-20pi')
print(looper.get_thresholds(thres_mode='minmax'))
M_0 = looper.results['V']

# get average Gaussian discord
params['solver']['measure_type'] = 'discord_G'
params['solver']['idx_e'] = (1, 3)
looper = wrap_looper(SystemClass=Bi00, params=params, func='mav', looper='x_looper', file_path='data/bi_00/discord_G_avg_1e3-20pi')
print(looper.get_thresholds(thres_mode='minmax'))
M_1 = looper.results['V']

# get Pearson correlation coefficient
params['solver']['measure_type'] = 'corr_ele'
params['solver']['idx_e'] = [(3, 3), (3, 7), (7, 7)]
looper = wrap_looper(SystemClass=Bi00, params=params, func='pcc', looper='x_looper', file_path='data/bi_00/pcc_1e3-20pi')
print(looper.get_thresholds(thres_mode='minmax'))
M_2 = looper.results['V']

# plotter
X = looper.axes['X']['val']
plotter = MPLPlotter(axes={
    'X': X,
    'Y': ['$\\langle S_{p} \\rangle$', '$5 \\times \\langle D_{G} \\rangle$', '$C$']
}, params=params['plotter'])
plotter.update(xs=X, vs=[M_0, [5 * m for m in M_1], M_2])
plotter.show(hold=True)