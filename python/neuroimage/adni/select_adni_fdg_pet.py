# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 19:25:47 2014

@author: mehdi
"""

import os
import pandas as pd

# read all adni pet list (from IDA search : original PET of all patient)
#filepath = os.path.join('csv', 'pet_original_559_idaSearch_10_14_2014.csv')
filepath = os.path.join('csv', 'pet_fdg_original_all_idaSearch_10_15_2014.csv')
pet_all = pd.read_csv(filepath)

''' Deprecated as the list already contains only fdg, baseline and 1 year
# extract FDG
fdg_idx = ['fdg' in d.lower() for d in pet_all['Description']]
pet_fdg = pet_all[fdg_idx]

# extract subject ID which have more than one FDG (longitudinal)
grouped = pet_fdg.groupby('Subject_ID')
pet_fdg_long = grouped.filter(lambda x: len(x) > 1)
'''

# extract baseline visits from the longitudinal fdg-pet
baseline_idx = ['baseline' in d.lower() for d in pet_all['Visit']]
pet_baseline = pet_all[baseline_idx]

# extract year 1 visits from the longitudinal fdg-pet
pet_year_1 = pd.DataFrame()
for year_1 in ['month 12', 'year 1']:
    year_1_idx = [year_1 in d.lower() for d in pet_all['Visit']]
    y1 = pet_all[year_1_idx]
    pet_year_1 = pet_year_1.append(y1, ignore_index=True)

# inner join the baseline and the year 1
pet_long = pd.merge(pet_baseline, pet_year_1, on='Subject_ID',
                    how='inner')

# get the list of subjects who have small