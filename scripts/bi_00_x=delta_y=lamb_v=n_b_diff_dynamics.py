# dependencies
import os 
import sys

# qom modules
from qom.utils.wrappers import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Bi00 import Bi00

# all parameters
params = {
    'looper': {
        'mode': 'serial',
        'X': {
            'var': 'delta',
            'min': - 0.02,
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
        'cache_dir': 'H:/Workspace/VSCode/Python/sync_bi_uni/data/bi_00/0.0_1000.0_10001',
        'method': 'ode',
        'measure_type': 'corr_ele',
        'idx_row': [2, 3, 6, 7],
        'idx_col': [2, 3, 6, 7],
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
        'type': 'pcolormesh',
        'palette': 'blr',
        'bins': 11,
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_bound': 'both',
        'x_ticks': [- 0.02, 0.00, 0.02],
        'y_label': '$\\lambda / \\omega_{mL}$',
        'y_bound': 'both',
        'y_ticks': [0.0, 0.04, 0.08],
        'cbar_title': '$n_{b_{R}} - n_{b_{L}}$',
        'cbar_ticks': [-100.0, 0.0, 100],
        'cbar_position': 'top',
        'label_font_size': 22,
        'tick_font_size': 18
    }
}

# function to obtain the difference between the phonon numbers
def func_n_b_diff(system_params, val, logger, results):
    # update system
    system = Bi00(system_params)
    # get correlations
    M_avg = system.get_measure_average(params['solver'], system.ode_func, system.get_ivc)
    # calculate difference
    n_b_diff = (M_avg[3] + M_avg[2] - M_avg[1] - M_avg[0]) / 2
    # update results
    results.append((val, n_b_diff))

# looper 
looper = wrap_looper(Bi00, params, func_n_b_diff, 'XYLooper', 'H:/Workspace/VSCode/Python/sync_bi_uni/data/bi_00/n_b_diff_1e3-20pi', True)
print(looper.get_thresholds('minmin'))