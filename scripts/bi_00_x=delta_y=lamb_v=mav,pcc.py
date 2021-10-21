# dependencies
import os 
import sys

# qom modules
from qom.utils.looper import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems import Bi00

# all parameters
params = {
    'looper': {
        'X': {
            'var': 'delta',
            'min': -0.02,
            'max': 0.02,
            'dim': 101
        },
        'Y': {
            'var': 'lamb',
            'min': 0.0,
            'max': 0.1,
            'dim': 101
        }
    },
    'solver': {
        'cache': True,
        'method': 'zvode',
        'measure_type': 'sync_p',
        'idx_e': (1, 3),
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
        'type': 'contourf',
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_ticks': [-0.02, 0.0, 0.02],
        'y_label': '$\\lambda / \\kappa$',
        'y_ticks': [0.0, 0.0375, 0.075],
        'y_tick_labels': [0.0, 0.25, 0.5],
        'width': 5.5,
        'height': 5.0
    }
}

# get average phase synchronization
params['solver']['measure_type'] = 'sync_p'
params['solver']['idx_e'] = (1, 3)
params['plotter']['palette'] = 'RdBu_r'
params['plotter']['cbar_title'] = '$\\langle S_{p} \\rangle$'
params['plotter']['cbar_ticks'] = [0.0, 0.1, 0.2]
looper = wrap_looper(SystemClass=Bi00, params=params, func='mav', looper='xy_looper', file_path='data/bi_00/sync_p_avg_1e3-20pi', plot=True)
print(looper.get_thresholds(thres_mode='minmax'))

# get average Gaussian discord
params['solver']['measure_type'] = 'discord_G'
params['solver']['idx_e'] = (1, 3)
params['plotter']['palette'] = 'Reds'
params['plotter']['cbar_title'] = '$\\langle D_{G} \\rangle$'
params['plotter']['cbar_ticks'] = [0.0, 0.01, 0.02]
looper = wrap_looper(SystemClass=Bi00, params=params, func='mav', looper='xy_looper', file_path='data/bi_00/discord_G_avg_1e3-20pi', plot=True)
print(looper.get_thresholds(thres_mode='minmax'))

# get Pearson correlation coefficient
params['solver']['measure_type'] = 'corr_ele'
params['solver']['idx_e'] = [(3, 3), (3, 7), (7, 7)]
params['plotter']['palette'] = 'Blues'
params['plotter']['cbar_title'] = '$C$'
params['plotter']['cbar_ticks'] = [0.0, 0.5, 1.0]
looper = wrap_looper(SystemClass=Bi00, params=params, func='pcc', looper='xy_looper', file_path='data/bi_00/pcc_1e3-20pi', plot=True)
print(looper.get_thresholds(thres_mode='minmax'))