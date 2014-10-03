# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 14:07:32 2014

@author: mehdi
"""

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Integration
res, err = quad(np.sin, 0, np.pi/2)

print np.allclose(res,1) # comparison with tolerance
print np.allclose(res,1)

# ODE

from scipy.integrate import odeint

def calc_deriv(ypos, time, counter_arr):
    counter_arr += 1
    return -2*ypos
    
counter=np.zeros((1,),dtype=np.uint16)

time_vec = np.linspace(0,4)
y_vec, info = odeint(calc_deriv, 1, time_vec, args=(counter,), full_output=True)
print info['nfe']
print counter

plt.close('all')
plt.plot(time_vec,y_vec)