# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 11:09:03 2014

@author: Mehdi
"""
import numpy as np
import pylab as pl


x=np.linspace(-10,10,10000)
y=np.cos(x)

pl.close('all')
pl.plot(x,y)