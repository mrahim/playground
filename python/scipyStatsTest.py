# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 13:23:14 2014

@author: mehdi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

a = np.random.normal(size=1000) #   norm
bins = np.arange(-4, 5)

histogram = np.histogram(a, bins=bins, normed=True)[0]
print histogram

bins = 0.5*(bins[1:] + bins[:-1])

plt.close('all')
plt.plot(bins,histogram)

b=stats.norm.pdf(bins)  #   norm
print b
plt.plot(bins,b)

#   fitting 
loc, std = stats.norm.fit(a)
print loc, std