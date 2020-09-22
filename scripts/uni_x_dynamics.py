#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Script to plot measure dynamics."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-09-22'
__updated__ = '2020-09-22'

# dependencies  
import json
import numpy as np
import os 
import sys
import scipy.integrate as si
import matplotlib.pyplot as plt

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'qom')))
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))
# import libraries
from qom.wrappers import dynamics
from qom.utils import axis

# import model
from models import uni_x

# load project data
data = {}
with open('sync_bi_uni.json') as data_file:
    data = json.load(data_file)
# extract model parameters
model_data = data['models']['uni']['00']
# extract dynamics data
script_data = data['scripts']

# initialize model
model = uni_x.Model00(model_data)

# calculate dynamics
dynamics.calculate(model, script_data)