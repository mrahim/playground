# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 15:15:26 2014

@author: mehdi
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def sixhumpcamelback(x,y):
    return (4-2.1*np.power(x,2)+np.power(x,4)/3)*np.power(x,2)+x*y+(4*np.power(y,2)-4)*np.power(y,2)

a=np.linspace(-2,2)
b=np.linspace(-1,1)

x,y=np.meshgrid(a,b) 

c = sixhumpcamelback(x,y)

print c

plt.close('all')
plt.imshow(c)

