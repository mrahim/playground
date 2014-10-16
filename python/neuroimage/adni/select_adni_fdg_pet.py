# -*- coding: utf-8 -*-
"""
A script that uses Pandas module to filter csv files of adni database
- subject list who have baseline and 1 year fdg-pet
- corresponding image list
"""

import os
import numpy as np
import pandas as pd

# read all adni pet list (from IDA search : original PET of all patient)
#filepath = os.path.join('csv', 'pet_original_559_idaSearch_10_14_2014.csv')
filepath = os.path.join('csv', 'search_results',
                        'pet_fdg_original_all_idaSearch_10_15_2014.csv')
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

# filter actual year 1
pet_long['Year_Diff'] = 0
for i in np.arange(len(pet_long)):
    dx = pet_long['Study_Date_x'][i][-4:]
    dy = pet_long['Study_Date_y'][i][-4:]
    pet_long['Year_Diff'][i] = int(dy) - int(dx)
pet_long_1 = pet_long[pet_long['Year_Diff'] < 2]
pet_long_1.to_csv(os.path.join('csv', 'pet_fdg_long_1.csv'))

# save image ids and subject_ids in "searchable" format
image_ids = pet_long_1['Image_ID_x'].append(pet_long_1['Image_ID_y'])
f = open(os.path.join('csv','pet_fdg_long_1_image_list'), 'w+')
image_ids.unique().tofile(f, sep=',')
f.close()

f = open(os.path.join('csv','pet_fdg_long_1_subject_list'), 'w+')
pet_long_1['Subject_ID'].unique().tofile(f, sep=',')
f.close()
