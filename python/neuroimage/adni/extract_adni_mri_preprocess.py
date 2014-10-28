# -*- coding: utf-8 -*-
"""
A script that uses Pandas module to search & copy files from adni directory.
- image list of baseline preprocessed T-1 MRI
"""

import os, glob, shutil
import pandas as pd


BASE_DIR = '/disk4t/mehdi/data/ADNI'
DST_BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'


filepath = os.path.join('csv', 'search_results',
                        'preprocessed_mri_10_27_2014.csv')
                        
mri_preproc_all = pd.read_csv(filepath)

image_ids = mri_preproc_all['Image_ID'].tolist()

# Check if the file exists (nii, xml)
# Search xml
file_list = glob.glob(BASE_DIR+'/*.xml')
file_df = pd.DataFrame(file_list, columns=['filepath'])

cfile_list = []
for image_id in image_ids:
    matching = ['I'+str(image_id)+'.xml' in fl for fl in file_df['filepath']]
    xml_file = file_df[matching]['filepath'].unique()
    if(len(xml_file) > 0):
        print image_id, xml_file[0]
        
        filename = os.path.split(xml_file[0])[1].split('.')[0]
        subject_id = '_'.join(filename.split('_', 4)[1:4])
        sequence_id = filename.rsplit('_', 2)[1]
        description = filename.split('_', 4)[4].rsplit('_', 2)[0]
        folderpath = os.path.join(BASE_DIR, subject_id, description)

        for root, dirs, files in os.walk(folderpath):
            for d in dirs:
                if d == str(sequence_id):
                    image_folder = os.path.join(root, d)
                    break
        print image_folder

        # Copy to a clean directory (nii, xml)
        dst_path = os.path.join(DST_BASE_DIR, 'I' + str(image_id))
        if(os.path.isdir(dst_path)):
            shutil.rmtree(dst_path)
        shutil.copytree(image_folder, dst_path)
        shutil.copy(xml_file[0], DST_BASE_DIR)
        cfile_list.append(image_id)

