#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Script to plot measure."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-06-19'
__updated__ = '2020-06-25'

# dependencies 
import json
import os 
import sys

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'qom')))
sys.path.append(os.path.abspath(os.path.join('..', 'sync_bi_uni')))

# import libraries
from qom.wrappers import measures

# import model
from models import bi

# load project data
data = {}
with open('sync_bi_uni.json') as data_file:
    data = json.load(data_file)
# extract model parameters
model_params = data['models']['bi']['00']['params']
# extract measure data
script_data = data['scripts']

# initialize model
model = bi.Model00(model_params)

# calculate the system dynamics
M, Thres, Axes = measures.calculate(model, script_data)