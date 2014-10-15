# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 19:25:47 2014

@author: mehdi
"""

import os
import numpy as np
import pandas as pd

# read all adni pet list
pet_all = pd.read_csv(
os.path.join('csv', 'pet_original_559_idaSearch_10_14_2014.csv'))

# extract FDG
fdg_idx = ['FDG' in d for d in pet_all['Description']]
pet_fdg = pet_all[fdg_idx]

# extract subject ID which have more than one FDG (longitudinal)
grouped = pet_fdg.groupby('Subject_ID')

pet_fdg_long = grouped.filter(lambda x: len(x)>1)

print pet_fdg_long.groupby('Visit').size()