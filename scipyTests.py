# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 14:59:11 2014

@author: mehdi
"""

import numpy as np
from scipy import io as spio

a = np.random.rand(4,4)
spio.savemat('matrix.mat', {'a':a})
print a

data = spio.loadmat('matrix.mat')
b = data['a']
print b