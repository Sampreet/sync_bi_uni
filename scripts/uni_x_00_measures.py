#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Script to plot measure."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-05-01'
__updated__ = '2020-08-25'

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

# calculate the system dynamics
M, Thres, Axes = measures.calculate(model, script_data)