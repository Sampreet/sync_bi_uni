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
        'method': 'zvode',
        'measure_type': 'corr_ele',
        'idx_e': [(2, 2), (3, 3), (6, 6), (7, 7)],
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
        'type': 'pcolormesh',
        'x_label': '$\\delta / \\omega_{mL}$',
        'x_ticks': [- 0.02, 0.00, 0.02],
        'y_label': '$\\lambda / \\kappa$',
        'y_ticks': [0.0, 0.0375, 0.075],
        'y_tick_labels': [0.0, 0.25, 0.5],
        'cbar_title': '$n_{b_{R}} - n_{b_{L}}$',
        'cbar_ticks': [-100.0, 0.0, 100],
        'cbar_position': 'top'
    }
}

# function to obtain the difference between the phonon numbers
def func_n_b_diff(system_params, val, logger, results):
    # update system
    system = Bi00(params=system_params)
    # get correlations
    M_avg = system.get_measure_average(solver_params=params['solver'])
    # calculate difference
    n_b_diff = (M_avg[3] + M_avg[2] - M_avg[1] - M_avg[0]) / 2
    # update results
    results.append((val, n_b_diff))

# # function to obtain the difference between the phonon numbers
# def func_n_b_diff(system_params, val, logger, results):
#     # update system
#     system = Bi00(system_params)
#     # get steady state values
#     _, corrs = system.get_modes_corrs_stationary(solver_params={})
#     # calculate difference
#     n_b_diff = (corrs[7][7] + corrs[6][6] - corrs[3][3] - corrs[2][2]) / 2
#     # update results
#     results.append((val, n_b_diff))

# looper 
looper = wrap_looper(SystemClass=Bi00, params=params, func=func_n_b_diff, looper='xy_looper', file_path='data/bi_00/n_b_diff_1e3-20pi', plot=True)
print(looper.get_thresholds('minmin'))