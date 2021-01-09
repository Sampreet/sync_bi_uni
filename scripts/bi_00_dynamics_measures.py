# dependencies
import json
import os 
import sys

# qom modules
from qom.ui import init_log
init_log()

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import system
from systems.Bi00 import Bi00

# import params
params = {}
with open('params/bi_00_dynamics_measure.json') as params_file:
    params = json.load(params_file)

# initialize system
system = Bi00(params['system'])

# get dynamics
M = system.get_dynamics_measure(params['solver'], system.ivc_func, system.ode_func, True, params['plotter'])