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
        'method_le': 'svd',
        'num_iters': 10000,
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
        'type': 'pcolormesh',
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_ticks': [-0.02, 0.0, 0.02],
        'y_label': '$\\lambda / \\kappa$',
        'y_ticks': [0.0, 0.0375, 0.075],
        'y_tick_labels': [0.0, 0.25, 0.5],
        'cbar_title': '$MLE$',
        'cbar_position': 'top',
        'cbar_ticks': [0, 0.0005, 0.001]
    }
}

# debug
print(params['looper'])

# wrapper
looper = wrap_looper(SystemClass=Bi00, params=params, func='les', looper='xy_looper', file_path='data/bi_00/les_1e3+10000')

# plotter
plotter = MPLPlotter(axes={
    'X': params['looper']['X'],
    'Y': params['looper']['Y']
}, params=params['plotter'])
plotter.update(vs=[[max(e) for e in r] for r in looper.results['V']])
plotter.show(True)