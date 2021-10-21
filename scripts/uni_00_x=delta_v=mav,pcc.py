# dependencies
import numpy as np
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
        'show_progress': True,
        'X': {
            'var': 'delta',
            'min': 0,
            'max': 0.01,
            'dim': 51
        }
    },
    'solver': {
        'cache': True,
        'method': 'zvode',
        'range_min': 99371,
        'range_max': 100001,
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
        'type': 'lines',
        'palette': 'RdBu_r',
        'bins': 21,
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_ticks': [0.00, 0.002, 0.004, 0.006, 0.008, 0.01],
        'y_sizes': [10, 10],
        'y_styles': ['-', '--', ':'],
        'v_label': '$C$',
        'v_ticks': [-1, -0.5, 0, 0.5, 1],
        'v_tick_labels': [-1, '', 0, '', 1],
        'width': 8.0,
        'height': 4.0
    }
}

# get average phase synchronization
params['solver']['measure_type'] = 'sync_p'
params['solver']['idx_e'] = (1, 3)
looper = wrap_looper(SystemClass=Uni00, params=params, func='mav', looper='x_looper', file_path='data/uni_00/sync_p_avg_1e4-20pi')
print(looper.get_thresholds(thres_mode='minmax'))
M_0 = looper.results['V']

# get Pearson synchronization
params['solver']['measure_type'] = 'corr_ele'
params['solver']['idx_e'] = [(3, 3), (3, 7), (7, 7)]
looper = wrap_looper(SystemClass=Uni00, params=params, func='pcc', looper='x_looper', file_path='data/uni_00/pcc_1e4-20pi')
print(looper.get_thresholds(thres_mode='minmax'))
M_1 = looper.results['V']

# plotter
X = looper.axes['X']['val']
plotter = MPLPlotter({
    'X': X
}, params['plotter'])
_colors = plotter.get_colors(palette=params['plotter']['palette'], bins=params['plotter']['bins'])
# get axis
ax = plotter.get_current_figure().axes[0]
# mark regions
ax.axvspan(0.0, 0.0023, color=_colors[10], alpha=0.5)
ax.axvspan(0.0023, 0.0033, color=_colors[4], alpha=0.5)
ax.axvspan(0.0033, 0.0039, color=_colors[10], alpha=0.5)
ax.axvspan(0.0039, 0.01, color=_colors[7], alpha=0.5)
# zero line
ax.plot(X, np.zeros(np.shape(X)), linestyle=':', color='k')
# right axis for phase synchronization
ax_right = plotter.get_twin_axis()
ax_right.set_ylabel('$\\langle S_{p} \\rangle$')
ax_right.set_ylim(0, 0.16)
ax_right.set_yticks([0, 0.08, 0.16])
ax_right.plot(X, M_0, linestyle='--', color='k')
# plot Pearson synchronization
ax.plot(X, M_1, linestyle='-', color=_colors[0])
ax.scatter(X, M_1, marker='o', color=_colors[0], s=15)
plotter.show(True)