'''
Parsing all subjects and saving estimated movements in a csv file:
    - 3 translations
    - 3 rotations
    - 3 quadratic translations
    - 3 cubic translations
    - 3 translations shifted 1 TR before
    - 3 translations shifted 1 TR after
'''

import os, glob
import numpy as np
import pandas as pd

BASE_DIR = os.path.join('/', 'home', 'Ppsypim', 'PSYDAT', 'Subjects')
DST_BASE_DIR = os.path.join('/', 'home', 'mr243268', 'dev',
                            'playground', 'python', 'neuroimage', 'eprime',
                            'movement_files')


for subject in os.listdir(BASE_DIR):
    mid_path = os.path.join(BASE_DIR, subject, 'MRI', 'MID')
    rp_files = glob.glob(os.path.join(mid_path, '*.txt'))
    if len(rp_files)>0:
        df = pd.read_csv(rp_files[0], sep='  ', names=['t_x', 't_y','t_z',
                                                       'r_x', 'r_y', 'r_z'])
        df['t_x_2'] = df['t_x']*df['t_x']
        df['t_y_2'] = df['t_y']*df['t_y']
        df['t_z_2'] = df['t_z']*df['t_z']
        
        df['t_x_3'] = df['t_x']*df['t_x']*df['t_x']
        df['t_y_3'] = df['t_y']*df['t_y']*df['t_y']
        df['t_z_3'] = df['t_z']*df['t_z']*df['t_z']
        
        df['t_x_s1'] = np.roll(df['t_x'], 1, axis=0)
        df['t_y_s1'] = np.roll(df['t_y'], 1, axis=0)
        df['t_z_s1'] = np.roll(df['t_z'], 1, axis=0)
        
        df['t_x_s2'] = np.roll(df['t_x'], -1, axis=0)
        df['t_y_s2'] = np.roll(df['t_y'], -1, axis=0)
        df['t_z_s2'] = np.roll(df['t_z'], -1, axis=0)
        
        df.to_csv(os.path.join(DST_BASE_DIR,
                               '_'.join([subject, 'reg.csv'])), sep=',')
                                                       