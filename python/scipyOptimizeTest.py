# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 14:45:24 2014

@author: mehdi
"""

import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

def f(x):
    return x**2 + 10*np.sin(x)
    


x = np.arange(-10, 10, 0.1)    
close('all')
plt.plot(x,f(x))
plt.show()

optimize.fmin_bfgs(f,3, disp=0) #local

grid = (-10, 10 , 0.1)
xmin=optimize.brute(f,(grid,)) #loop
print xmin


root = optimize.fsolve(f,1) #find roots
print root


xd = np.linspace(-10,10)
yd = f(xd) + np.random.randn(xd.size)


def f2(x,a,b):
    return a*x**2 + b*np.sin(x)

guess = [2,2]
params, params_cov = optimize.curve_fit(f2, xd, yd, guess)

print params


