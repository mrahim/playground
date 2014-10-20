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

