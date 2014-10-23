# -*- coding: utf-8 -*-
"""
A script that uses Pandas module to filter csv files of adni database
- subject list who have baseline and 1 year processed fdg-pet
- corresponding processed image list
"""

import os
import numpy as np
import pandas as pd

'''
read all adni fdg pet processed list 
(from IDA search : processed PET of all patient longitudinal acq)
'''
filepath = os.path.join('csv', 'search_results',
                        'pet_fdg_processed_idaSearch_10_20_2014.csv')
pet_proc_all = pd.read_csv(filepath)

pet_proc_baseline = pet_proc_all[(pet_proc_all.Visit == 'ADNI1 Baseline')]


fdg_idx = ['fdg' in d.lower() for d in pet_proc_baseline['Description']]
pet_proc_baseline = pet_proc_baseline[fdg_idx]

pet_proc_avg_baseline = pd.DataFrame()
keys = ['uniform'] # Kind of processed images ? (registered,averaged,uniform)
for key in keys:
    avg_idx = [key in d.lower() for d in pet_proc_baseline['Description']]
    pet_proc_avg_baseline = pet_proc_avg_baseline.append(pet_proc_baseline[avg_idx])
    
pet_proc_avg_baseline = pet_proc_avg_baseline.drop_duplicates(['Subject_ID'])

pet_proc_avg_baseline.to_csv(os.path.join('csv', 'pet_proc_fdg_baseline.csv'))


# save image ids and subject_ids in "searchable" format
f = open(os.path.join('csv','pet_proc_fdg_baseline_image_list'), 'w+')
pet_proc_avg_baseline['Image_ID'].unique().tofile(f, sep=',')
f.close()
