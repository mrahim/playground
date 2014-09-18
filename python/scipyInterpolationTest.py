# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 15:42:46 2014

@author: mehdi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


# basic noisy function
m_time = np.linspace(0,1,10)
noise = (np.random.random(10)*2 -1)*1e-1
measures = np.sin(2*np.pi*m_time)+noise

plt.close('all')
plt.plot(m_time,measures)


# interpolation of the measures
linear_interp = interpolate.interp1d(m_time, measures, kind='linear')
cubic_interp = interpolate.interp1d(m_time, measures, kind='cubic')

c_time = np.linspace(0,1)
plt.plot(c_time,linear_interp(c_time))
plt.plot(c_time,cubic_interp(c_time))



