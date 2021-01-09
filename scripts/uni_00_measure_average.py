# dependencies
import json
import numpy as np
import os 
import sys

# qom modules
from qom.loopers import XYLooper
from qom.ui import init_log
init_log()

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Uni00 import Uni00

# import params
params = {}
with open('params/uni_00_measure_average.json') as params_file:
    params = json.load(params_file)

# initialize system
system = Uni00(params['system'])

def func(system_params, val, logger, results):
    # update parameters
    system.params = system_params
    # get result
    res = system.get_measure_average(params['solver'])
    # update results
    results.append((val, res))

# looper
looper = XYLooper(func, params)
_file = 'data\\uni_00\\S_P_' + str(params['solver']['range_min']) + '_' + str(params['solver']['range_max'])

# load
if os.path.isfile(_file + '.npz'):
    _data = np.load(_file + '.npz')
    looper.results = {
        'X': _data['X'].tolist(),
        'Y': _data['Y'].tolist(),
        'V': _data['V'].tolist()
    }
# save
else:
    looper.loop()
    _xs = np.array(looper.results['X'])
    _ys = np.array(looper.results['Y'])
    _vs = np.array(looper.results['V'])
    np.savez_compressed(_file, X=_xs, Y=_ys, V=_vs)

# plot
looper.plot_results()