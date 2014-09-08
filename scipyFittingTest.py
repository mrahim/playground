# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 15:15:26 2014

@author: mehdi
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def sixhumpcamelback(X):
    return (4-2.1*np.power(X[0],2)+np.power(X[0],4)/3)*np.power(X[0],2)+X[0]*X[1]+(4*np.power(X[1],2)-4)*np.power(X[1],2)

a=np.linspace(-2,2)
b=np.linspace(-1,1)

x,y=np.meshgrid(a,b) 

c = sixhumpcamelback([x,y])

print y.shape

plt.close('all')
plt.imshow(c)
plt.colorbar()

R = optimize.fmin_bfgs(sixhumpcamelback, [0.1,0.1])

R1 = (R[0]+2)*50/4
R2 = (R[1]+1)*50/2
print R

plt.scatter(R1,R2)