# dependencies
import os 
import sys

# qom modules
from qom.ui.plotters import MPLPlotter
from qom.utils.looper import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems import Uni00

# all parameters
params = {
    'looper': {
        'X': {
            'var': 'delta',
            'min': 0.00,
            'max': 0.02,
            'dim': 101
        },
        'Y': {
            'var': 'eta',
            'min': 0.5,
            'max': 1.0,
            'dim': 101
        }
    },
    'solver': {
        'cache': True,
        'method': 'zvode',
        'method_le': 'svd',
        'num_iters': 10000,
        't_min': 0.0,
        't_max': 10000.0,
        't_dim': 100001
    },
    'system': {
        'A_l': 52.0,
        'Delta_0': 1.0, 
        'delta': 0.005, 
        'eta': 0.75,
        'g_0s': [0.005, 0.005],
        'gammas': [0.005, 0.005],
        'kappas': [0.15, 0.15],
        'n_ths': [0, 0],
        'omega_m': 1.0
    },
    'plotter': {
        'type': 'pcolormesh',
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_ticks': [0.00, 0.01, 0.02],
        'y_label': '$\\eta$',
        'y_ticks': [0.5, 0.75, 1.0],
        'cbar_title': '$MLE$',
        'cbar_position': 'top',
        'cbar_ticks': [0, 0.001, 0.002]
    }
}

# debug
print(params['looper'])

# wrapper
looper = wrap_looper(SystemClass=Uni00, params=params, func='les', looper='xy_looper', file_path='data/uni_00/les_1e4+10000')

# plotter
plotter = MPLPlotter(axes={
    'X': params['looper']['X'],
    'Y': params['looper']['Y']
}, params=params['plotter'])
plotter.update(vs=[[max(e) for e in r] for r in looper.results['V']])
plotter.show(True)