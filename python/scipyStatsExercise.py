# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 14:01:34 2014

@author: mehdi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# Data generation
b = np.random.gamma(1,size=1000)

# Create histogram
bins = np.arange(0,10)
histogram = np.histogram(b, bins, normed=True)[0]

bins = 0.5*(bins[1:] + bins[:-1])

plt.close('all')
plt.plot(bins,histogram)


# Using stats.gamma
bins = np.arange(0,10)
g = stats.gamma.pdf(bins,1)
plt.plot(bins,g)
