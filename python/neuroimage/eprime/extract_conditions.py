# -*- coding: utf-8 -*-
"""
A script that extracts the conditions from eprime csv file :
    *
    - Anticip_hit_largewin
    - Anticip_hit_smallwin
    - Anticip_hit_nowin
    - Anticip_missed_largewin
    - Anticip_missed_smallwin
    - Anticip_missed_nowin
    - Anticip_noresp
    *
    - Feedback_hit_largewin
    - Feedback_hit_smallwin
    - Feedback_hit_nowin
    - Feedback_missed_largewin
    - Feedback_missed_smallwin
    - Feedback_missed_nowin
    - Feedback_noresp
    *
    - Press_left
    - Press_right
"""

import os
import numpy as np
import pandas as pd

# Load eprime csv file
filename = os.path.join('/home', 'mr243268', 'dev', 'playground', 'python',
                        'neuroimage', 'eprime', 'eprime_files', 'csv',
                        'c_MIDT_forscan-10119-1.csv')
df = pd.read_csv(filename)

'''
Extract hits, misses and noresps
'''
# hits
hit = np.zeros(len(df))
h_idx = df[df['PictureTarget.CRESP'] == df['PictureTarget.RESP']]['TrialList']
hit[h_idx.unique()-1] = 1

# noresps
noresp = np.zeros(len(df))
n_idx = df[df['PictureTarget.RESP'].isnull()]['TrialList']
noresp[n_idx.unique()-1] = 1

# misses
miss = np.zeros(len(df))
m_idx = df[df['PictureTarget.CRESP'] + df['PictureTarget.RESP'] == 9 ]['TrialList']
miss[m_idx.unique()-1] = 1

'''
Extract bigwins, smallwins and nowins
'''
# big wins
bigwin = np.zeros(len(df))
bw_idx = df[df['prize']==10]['TrialList']
bigwin[bw_idx.unique()-1] = 1

# small wins
smallwin = np.zeros(len(df))
sw_idx = df[df['prize']==2]['TrialList']
smallwin[sw_idx.unique()-1] = 1

# no wins
nowin = np.zeros(len(df))
nw_idx = df[df['prize']==0]['TrialList']
nowin[nw_idx.unique()-1] = 1

