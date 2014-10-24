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

"""
Extract hits, misses and noresps
"""
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

"""
Extract bigwins, smallwins and nowins
"""
# big wins
largewin = np.zeros(len(df))
lw_idx = df[df['prize']==10]['TrialList']
largewin[lw_idx.unique()-1] = 1

# small wins
smallwin = np.zeros(len(df))
sw_idx = df[df['prize']==2]['TrialList']
smallwin[sw_idx.unique()-1] = 1

# no wins
nowin = np.zeros(len(df))
nw_idx = df[df['prize']==0]['TrialList']
nowin[nw_idx.unique()-1] = 1

"""
Extract press left (5), press right (4)
"""
# press left
pleft = np.zeros(len(df))
pl_idx = df[df['PictureTarget.CRESP'] == 5]['TrialList']
pleft[pl_idx.unique()-1] = 1

# press right
pright = np.zeros(len(df))
pr_idx = df[df['PictureTarget.CRESP'] == 4]['TrialList']
pright[pr_idx.unique()-1] = 1

"""
Extract times
"""
anticip_start_time = df['PicturePrime.OnsetTime']/1000.
response_time = df['PictureTarget.RTTime']/1000.
feedback_start_time = (df['PictureTarget.OnsetTime'] + df['Target_time'])/1000.

"""
Compute conditions
"""
cond = pd.DataFrame({'hit': hit,
                     'miss': miss,
                     'noresp': noresp,
                     'largewin': largewin,
                     'smallwin': smallwin,
                     'nowin': nowin,
                     'pleft': pleft,
                     'pright': pright,
                     'response_time': response_time,
                     'anticip_start_time': anticip_start_time,
                     'feedback_start_time': feedback_start_time
                     })

print cond[(hit==1) & (largewin==1)]['anticip_start_time']

# hit, largewin
