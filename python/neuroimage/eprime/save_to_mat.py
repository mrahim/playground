# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 21:15:15 2014

@author: Mehdi
"""
import numpy as np
from scipy import io
from collections import OrderedDict

def generate_multiconditions_mat(output_file, conditions, ddurations):
    names = np.zeros((len(conditions),), dtype=np.object)
    onsets = np.zeros((len(conditions),), dtype=np.object)
    durations = np.zeros((len(conditions),), dtype=np.object)
    for i in np.arange(0, len(conditions)):
        names[i] = conditions.keys()[i]
        onsets[i] = conditions[names[i]]
        durations[i] = ddurations[names[i]]

    return names, onsets, durations


anticip = np.random.rand(5)*100
feedback = np.random.rand(5)*100
click = np.random.rand(2)*100
nada = np.random.rand(1)*100



conditions = {'anticip': anticip,
              'feedback': feedback,
              'click': click,
              'nada': nada}              

ddurations = {'anticip': 2.,
             'feedback': 5.,
             'click': 0.,
             'nada': 0.}

names, onsets, durations = generate_multiconditions_mat(conditions, ddurations)

io.savemat('test', {'names' : names,
                    'onsets' : onsets,
                    'durations' : durations})
print names, onsets, durations 
'''
names
onsets
durations

obj_arr = np.zeros((2,), dtype=np.object)
obj_arr[0] = [1, 2]
obj_arr[1] = 'a string'


io.savemat('test', {'cond':obj_arr})

'''