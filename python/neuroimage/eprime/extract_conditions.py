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
from nipy.modalities.fmri import design_matrix
from nipy.modalities.fmri.experimental_paradigm import BlockParadigm

# Load eprime csv file
filename = os.path.join('/Users', 'Mehdi', 'Codes', 'dev', 'playground', 'python',
                        'neuroimage', 'eprime', 'eprime_files', 'csv',
                        'c_MIDT_forscan-10119-1.csv')

for f in [filename]:

    df = pd.read_csv(f)

    """
    Set event durations
    """
    anticip_duration = 4.
    feedback_duration = 1.5
    
    """
    Extract hits, misses and noresps
    """
    # hits
    hit = np.zeros(len(df))
    h_idx = df[df['PictureTarget.CRESP'] == df['PictureTarget.RESP']]['TrialList']
    hit[h_idx.values - 1] = 1
    
    # noresps
    noresp = np.zeros(len(df))
    n_idx = df[df['PictureTarget.RESP'].isnull()]['TrialList']
    noresp[n_idx.values - 1] = 1
    
    # misses
    miss = np.zeros(len(df))
    m_idx = df[df['PictureTarget.CRESP'] + df['PictureTarget.RESP'] == 9 ]['TrialList']
    miss[m_idx.values - 1] = 1
    
    """
    Extract bigwins, smallwins and nowins
    """
    # big wins
    largewin = np.zeros(len(df))
    lw_idx = df[df['prize']==10]['TrialList']
    largewin[lw_idx.values - 1] = 1
    
    # small wins
    smallwin = np.zeros(len(df))
    sw_idx = df[df['prize']==2]['TrialList']
    smallwin[sw_idx.values - 1] = 1
    
    # no wins
    nowin = np.zeros(len(df))
    nw_idx = df[df['prize']==0]['TrialList']
    nowin[nw_idx.values - 1] = 1
    
    """
    Extract press left (5), press right (4)
    """
    # press left
    pleft = np.zeros(len(df))
    pl_idx = df[df['PictureTarget.RESP'] == 5]['TrialList']
    pleft[pl_idx.values - 1] = 1
    
    # press right
    pright = np.zeros(len(df))
    pr_idx = df[df['PictureTarget.RESP'] == 4]['TrialList']
    pright[pr_idx.values - 1] = 1
    
    """
    Extract times
    """
    anticip_start_time = df['PicturePrime.OnsetTime']/1000.
    response_time = df['PictureTarget.RTTime']/1000.
    feedback_start_time = (df['PictureTarget.OnsetTime'] + df['Target_time'])/1000.
    
    """
    Compute conditions
    """
    cond = pd.DataFrame({'response_time': response_time,
                         'anticip_start_time': anticip_start_time,
                         'feedback_start_time': feedback_start_time})
    
    # Anticipation
    anticip_hit_largewin = cond[(hit==1) & (largewin==1)]['anticip_start_time'].values
    anticip_hit_smallwin = cond[(hit==1) & (smallwin==1)]['anticip_start_time'].values
    anticip_hit_nowin = cond[(hit==1) & (nowin==1)]['anticip_start_time'].values
    anticip_hit = np.hstack((anticip_hit_largewin,
                             anticip_hit_smallwin, anticip_hit_nowin))
    anticip_hit_modgain = np.hstack([[3.]*len(anticip_hit_largewin),
                                     [2.]*len(anticip_hit_smallwin),
                                     [1.]*len(anticip_hit_nowin)])
    
    anticip_missed_largewin = cond[(miss==1) & (largewin==1)]['anticip_start_time'].values
    anticip_missed_smallwin = cond[(miss==1) & (smallwin==1)]['anticip_start_time'].values
    anticip_missed_nowin = cond[(miss==1) & (nowin==1)]['anticip_start_time'].values
    anticip_missed = np.hstack((anticip_missed_largewin,
                                anticip_missed_smallwin, anticip_missed_nowin))
    anticip_missed_modgain = np.hstack([[3.]*len(anticip_missed_largewin),
                                        [2.]*len(anticip_missed_smallwin),
                                        [1.]*len(anticip_missed_nowin)])
    
    anticip_noresp = cond[(noresp==1)]['anticip_start_time'].values
    
    # Feedback
    feedback_hit_largewin = cond[(hit==1) & (largewin==1)]['feedback_start_time'].values
    feedback_hit_smallwin = cond[(hit==1) & (smallwin==1)]['feedback_start_time'].values
    feedback_hit_nowin = cond[(hit==1) & (nowin==1)]['feedback_start_time'].values
    feedback_hit = np.hstack((feedback_hit_largewin,
                              feedback_hit_smallwin, feedback_hit_nowin))
    feedback_hit_modgain = np.hstack([[3.]*len(feedback_hit_largewin),
                                     [2.]*len(feedback_hit_smallwin),
                                     [1.]*len(feedback_hit_nowin)])
    
    feedback_missed_largewin = cond[(miss==1) & (largewin==1)]['feedback_start_time'].values
    feedback_missed_smallwin = cond[(miss==1) & (smallwin==1)]['feedback_start_time'].values
    feedback_missed_nowin = cond[(miss==1) & (nowin==1)]['feedback_start_time'].values
    feedback_missed = np.hstack((feedback_missed_largewin,
                                 feedback_missed_smallwin, feedback_missed_nowin))
    feedback_missed_modgain = np.hstack([[3.]*len(feedback_missed_largewin),
                                        [2.]*len(feedback_missed_smallwin),
                                        [1.]*len(feedback_missed_nowin)])
    
    feedback_noresp = cond[(noresp==1)]['feedback_start_time'].values
    
    # Response
    press_left = cond[(pleft==1)]['response_time'].values
    press_right = cond[(pright==1)]['response_time'].values
    
    # namelist
    namelist = ['anticip_hit', 'anticip_missed', 'anticip_noresp',
                'feedback_hit', 'feedback_missed', 'feedback_noresp',
                'press_left', 'press_right']
    
    modulationnamelist = ['anticip_hit_modgain', 'anticip_missed_modgain', 
                          'feedback_hit_modgain', 'feedback_missed_modgain']

    # Create paradigms
    
    block_cond = {'anticip_hit_largewin' : anticip_hit_largewin,
                  'anticip_hit_smallwin' : anticip_hit_smallwin,
                  'anticip_hit_nowin' : anticip_hit_nowin,
                  'anticip_missed_largewin' : anticip_missed_largewin,
                  'anticip_missed_smallwin' : anticip_missed_smallwin,
                  'anticip_missed_nowin' : anticip_missed_nowin,
                  'anticip_noresp' : anticip_noresp,
                  'feedback_hit_largewin' : feedback_hit_largewin,
                  'feedback_hit_smallwin' : feedback_hit_smallwin,
                  'feedback_hit_nowin' : feedback_hit_nowin,
                  'feedback_missed_largewin' : feedback_missed_largewin,
                  'feedback_missed_smallwin' : feedback_missed_smallwin,
                  'feedback_missed_nowin' : feedback_missed_nowin,
                  'feedback_noresp' : feedback_noresp}
                  

    condition = []
    onset = []
    for c in block_cond:
        condition += [c]*len(block_cond[c])
        print c, len(block_cond[c])
        onset = np.hstack([onset, block_cond[c]])
    durations = [4.]*len(condition)
    b_paradigm = BlockParadigm(con_id=condition,
                               onset = onset,
                               duration = durations)    
                               
    frametimes = np.linspace(0,800,800)
    
    design_mat = design_matrix.make_dmtx(frametimes, b_paradigm,
                                     hrf_model='Canonical',
                                     drift_model='Cosine',
                                     hfcut=128)
    design_mat.show()
