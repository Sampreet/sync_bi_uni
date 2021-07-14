# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.ui.plotters import MPLPlotter
from qom.utils.wrappers import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Uni00 import Uni00
from systems.Uni01 import Uni01

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
        'cache_dir': 'H:/Workspace/VSCode/Python/sync_bi_uni/data/uni_00/0.0_10000.0_100001',
        'method': 'ode',
        'range_min': 99371,
        'range_max': 100001,
        't_min': 0,
        't_max': 10000,
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
        'x_bound': 'both',
        'x_ticks': [0.00, 0.002, 0.004, 0.006, 0.008, 0.01],
        'y_sizes': [10, 10],
        'y_styles': ['--', '-', ':'],
        'v_label': '$10^{3} \\times TLE$',
        'v_bound': 'both',
        'v_ticks': [-0.0015, -0.001, -0.0005, 0.000, 0.0005],
        'v_tick_labels': ['', -1, '', 0, ''],
        'label_font_size': 22,
        'tick_font_size': 18
    }
}

# get average phase synchronization
params['solver']['measure_type'] = 'qcm'
params['solver']['qcm_type'] = 'sync_phase'
params['solver']['idx_mode_i'] = 1
params['solver']['idx_mode_j'] = 3
looper = wrap_looper(Uni00, params, 'measure_average', 'XLooper', 'data/uni_00/S_phase_avg_1e4-20pi')
print(looper.get_thresholds(thres_mode='minmax'))
S_phase_avg = looper.results['V']

# get transverse Lyapunov exponents
params['solver']['idx_eig'] = [6, 7]
looper = wrap_looper(Uni01, params, 'eig_max', 'XLooper', 'data/uni_00/Eig_max_1e4-20pi')
print(looper.get_thresholds(thres_mode='minmax'))
Eig_max = looper.results['V']

# plotter
X = looper.axes['X']['val']
plotter = MPLPlotter({
    'X': X
}, params['plotter'])
_colors = plotter.axes['Y'].colors
# get axis
ax = plotter.get_current_figure().axes[0]
# mark regions
ax.axvspan(0.0, 0.0023, color=_colors[10], alpha=0.5)
ax.axvspan(0.0023, 0.0033, color=_colors[-5], alpha=0.5)
ax.axvspan(0.0033, 0.0039, color=_colors[10], alpha=0.5)
ax.axvspan(0.0039, 0.01, color=_colors[-8], alpha=0.5)
# zero line
ax.plot(X, np.zeros(np.shape(X)), linestyle=':', color='k')
# right axis for phase synchronization
ax_right = plotter.get_twin_axis()
ax_right.set_ylabel('$\\langle S_{p} \\rangle$')
ax_right.set_ylim(0, 0.16)
ax_right.set_yticks([0, 0.08, 0.16])
ax_right.plot(X, S_phase_avg, linestyle='--', color='k')
# plot transverse Lyapunov exponents
ax.plot(X, Eig_max, linestyle='-', color=_colors[-3])
ax.scatter(X, Eig_max, marker='o', color=_colors[-3], s=15)
plotter.show(True, 7.5, 3.0)