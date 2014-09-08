# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 14:32:31 2014

@author: mehdi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

a = np.random.normal(0, 1, size=100)
b = np.random.normal(1, 1, size=10)



[t,prob] = stats.ttest_ind(b,a)

print "a :\n",mean(a),np.std(a),"\nb:\n",mean(b),np.std(b),"\nt,prob:\n",t,prob

