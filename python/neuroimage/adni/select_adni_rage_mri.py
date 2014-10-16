# -*- coding: utf-8 -*-
"""
A script that uses Pandas module to filter on csv files of adni database
- unique subject list
- distribution of the downloaded data (Groups, Modalities, Sex, ...)
"""

import numpy as np
import pandas as pd

# Read input files
fp = pd.read_csv('csv/search_results/fmri_and_pet_idaSearch_10_07_2014.csv')
fpm = pd.read_csv('csv/search_results/fmri_and_pet_and_mri_idaSearch_10_07_2014.csv')
mri = pd.read_csv('csv/search_results/mri_idaSearch_10_08_2014.csv')

# Get unique subject ids
f = open('csv/fmri_and_pet_subject_list', 'w+')
fp['Subject_ID'].unique().tofile(f, sep=',')
f.close()


# Get MRI ids of *RAGE* type
keyword = 'RAGE'
matching = [keyword in s for s in mri['Description']]

f = open('csv/mri_rage_list', 'w+')
mri[matching]['Image_ID'].unique().tofile(f, sep=',')
f.close()
selected_mri = mri[matching]

# Get informations for the selected subjects
all_info = pd.read_csv('csv/search_results/all_informations_idaSearch_10_06_2014.csv')
subject_ids = fpm['Subject_ID'].unique()



# Select: *RAGE* MRI, PET, fMRI
matching = [keyword in s for s in fpm['Description']]
selected_fpm = fpm[(matching) | (fpm['Modality'] == 'PET')
                              | (fpm['Modality'] == 'fMRI')]

selected_fpm.to_csv('csv/selected_fmri_pet_mri.csv')

# Display fMRI and PET distribution
for mod in ['fMRI', 'PET']:
    print selected_fpm[
    (selected_fpm.Modality == mod)].groupby('Description').size()

# Display PET types
selected_pet = selected_fpm[selected_fpm['Modality'] == 'PET']
f = open('csv/pet_description_list', 'w+')
selected_pet['Description'].unique().tofile(f, sep='\n')
f.close()
for typ in ['AV', 'FDG', 'PIB']:
    matching = [typ in s for s in selected_pet['Description']]
    print '--\n', typ, ': ', selected_pet[matching]['Image_ID'].unique().shape

# Extract the subjects from the sub-list
selected_subjects = selected_fpm.drop_duplicates(subset='Subject_ID')

for key in ['Sex', 'DX_Group']:
    print '--\n', selected_subjects.groupby(key).size()

print '--\n', selected_subjects.groupby('DX_Group').agg({'Age': np.mean})

print '--\nPET\n', selected_pet.groupby('Phase').size()
print '--\nMRI\n', selected_mri.groupby('Phase').size()




# TODO : Modality repartition histogram of the subjects
