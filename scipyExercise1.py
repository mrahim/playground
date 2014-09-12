# -*- coding: utf-8 -*-
"""

:Exercise 1: Maximum wind speed prediction
:Synopsis: The exercise goal is to predict the maximum wind speed occurring 
every 50 years even if no measure exists for such a period. 
The available data are only measured over 21 years at the Sprogø 
meteorological station located in Denmark. 
First, the statistical steps will be given and then illustrated 
with functions from the scipy.interpolate module.
:Author: RAHIM Mehdi

"""

import numpy as np
import pylab as pl
from scipy.interpolate import UnivariateSpline


max_speeds = np.load('max-speeds.npy')


nb_years = max_speeds.shape[0]
cprob = (np.arange(nb_years, dtype=np.float32)+1)/(nb_years+1)

sorted_max_speeds = np.sort(max_speeds)

quantile_func = UnivariateSpline(cprob, sorted_max_speeds)

nprob = np.linspace(0,1,1e2)
fitted_max_speed = quantile_func(nprob)

fifty_prob = 1. -0.02
fifty_wind = quantile_func(fifty_prob)

print fifty_wind


pl.close('all')
pl.plot(fitted_max_speed,nprob,'--g')

pl.plot(sorted_max_speeds,cprob,linestyle='',marker='o',markerfacecolor='blue')
pl.xlabel('Max Wind Speed')
pl.ylabel('Cumulative probability')








