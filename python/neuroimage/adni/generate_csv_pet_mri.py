# -*- coding: utf-8 -*-
"""
A script that generates a csv info file from data directory
"""

import os, glob
import pandas as pd

BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'
BASE_DIR = ''

mri_filepath = os.path.join('csv', 'search_results',
                        'maper_segmented_mri_10_21_2014.csv')
mri_all = pd.read_csv(mri_filepath)


pet_filepath = filepath = os.path.join('csv', 'search_results',
                        'pet_fdg_processed_idaSearch_10_20_2014.csv')                        
pet_all = pd.read_csv(pet_filepath)

list_id = glob.glob(BASE_DIR+'/I*')
image_ids = []
for d in list_id:
    image_ids.append(int(d.split('/')[-1][1:]))

mri = mri_all[mri_all['Image_ID'].isin(image_ids)]
pet = pet_all[pet_all['Image_ID'].isin(image_ids)]

selected_images = pd.merge(mri, pet, on='Subject_ID')

          
fields = ['Subject_ID', 'Image_ID_x', 'Image_ID_y', 'Sex_x', 'Age_x', 'Phase',
          'Study_Date', 'Visit_x', 'Modality_x', 'Modality_y',
       'Description_x', 'Type_x', 'Acq_Date', 'Format', 'Sex_y',
       'Weight', 'Research_Group', 'APOE_A2', 'APOE_A1', 'DX_Group', 'Visit_y',
        'Age_y', 'Global_CDR',
       'Modified_Hachinski_Total_Score', 'NPI-Q_Total_Score', 'MMSE_Total_Score',
       'Functional_Assessment_Questionnaire_Total_Score',
       'GDSCALE_Total_Score', 'Description_y', 'Type_y',
       'Imaging_Protocol', 'Tissue', 'Laterality', 'Registration',
       'Structure', 'Image_Type']
          
selected_images[fields].to_csv(os.path.join(BASE_DIR, 'description_file.csv'))
