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

import os, glob
from collections import OrderedDict
import numpy as np
from scipy import io
import matplotlib.pyplot as plt
import pandas as pd
from nipy.modalities.fmri import design_matrix
from nipy.modalities.fmri.experimental_paradigm import BlockParadigm


def check_eprime_subject(eprime_file, mapping):
    """
        A temporary function that checks if the eprime id
        has an existing corresponding subject
    """
    eprime_nb = eprime_file.split('/')[-1].split('.')[0].rsplit('-')[-2]
    res = mapping[mapping['eprime'] == int(eprime_nb)]['subject'].values
    return res


def generate_multiregressors_mat(output_file, regressors):
    """
        Generate a *.mat file that contains the regressors
    """
    io.savemat(output_file, {'R': regressors})

def generate_multiconditions_mat(output_file, conditions, ddurations):
    """
        Generate a *.mat file that contains the names, the onsets
        and the durations, according to SPM's mutiple coditions file
    """
    names = np.zeros((len(conditions),), dtype=np.object)
    onsets = np.zeros((len(conditions),), dtype=np.object)
    durations = np.zeros((len(conditions),), dtype=np.object)
    for i in np.arange(0, len(conditions)):
            names[i] = conditions.keys()[i]
            print names[i]
            onsets[i] = conditions[names[i]]
            durations[i] = ddurations[names[i]]
    io.savemat(output_file, {'names' : names,
                             'onsets' : onsets,
                             'durations' : durations})
    return names, onsets, durations


BASE_DIR = '/Users/Mehdi/Codes'
BASE_DIR = '/home/mr243268'

N_SCANS = 289
TR = 2.4

# Load eprime csv file
filename = os.path.join(BASE_DIR, 'dev', 'playground', 'python',
                        'neuroimage', 'eprime', 'eprime_files', 'csv',
                        'c_MIDT_forscan-10119-1.csv')


file_list = glob.glob(os.path.join(BASE_DIR, 'dev', 'playground', 'python',
                        'neuroimage', 'eprime', 'eprime_files', 'csv',
                        'c_*.csv'))

for f in file_list:

    df = pd.read_csv(f)

    # Set event durations
    anticip_duration = 4.
    feedback_duration = 1.45
    
    # Extract hits, misses and noresps
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
    
    # Extract bigwins, smallwins and nowins
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
    

    # Extract press left (5), press right (4)
    # press left
    pleft = np.zeros(len(df))
    pl_idx = df[df['PictureTarget.RESP'] == 5]['TrialList']
    pleft[pl_idx.values - 1] = 1
    
    # press right
    pright = np.zeros(len(df))
    pr_idx = df[df['PictureTarget.RESP'] == 4]['TrialList']
    pright[pr_idx.values - 1] = 1
    
    # Extract times
    first_onset = df['PicturePrime.OnsetTime'][0]
    start_delay = 6000
    anticip_start_time = (df['PicturePrime.OnsetTime'] - first_onset + start_delay - 2 * TR)/1000.
    response_time = (df['PictureTarget.RTTime'] - first_onset + start_delay - 2 * TR)/1000.
    feedback_start_time = (df['PictureTarget.OnsetTime'] + df['Target_time'] - first_onset + start_delay - 2 * TR)/1000.
    
    # Compute conditions
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

    # Load regressors
    mapping = pd.read_csv(os.path.join('/','home','mr243268',
                                       'dev','playground','python',
                                       'neuroimage','eprime','mapping.csv'),
                          names=['eprime','subject'])
    
    subject_id = check_eprime_subject(f, mapping)
    if len(subject_id)>0:
        print subject_id[0]
        filepath = os.path.join('/','home','mr243268',
                                'dev','playground','python',
                                'neuroimage','eprime',
                                'movement_files', 
                                ''.join(['S',str(subject_id[0]),
                                '_reg.csv']))
        if os.path.isfile(filepath):
            reg = pd.read_csv(filepath)
            regressors = reg.values[:,1:]
            output_file = os.path.join(BASE_DIR, 'dev', 'playground', 'python',
                                       'neuroimage', 'eprime', 'eprime_files',
                                       'mat', ''.join(['S',str(subject_id[0]),'_reg']))
            generate_multiregressors_mat(output_file, regressors)
    

    # Create paradigms   
    conditions =  OrderedDict()
    """
    conditions = {'anticip_hit_largewin' : anticip_hit_largewin,
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
                  'feedback_noresp' : feedback_noresp,
                  'press_left' : press_left,
                  'press_right' : press_right}
                  
 conditions = {'anticip_hit_largewin' : anticip_hit_largewin,
                  'anticip_hit_smallwin' : anticip_hit_smallwin,
                  'anticip_hit_nowin' : anticip_hit_nowin,
                  'anticip_noresp' : anticip_noresp,
                  'feedback_hit_largewin' : feedback_hit_largewin,
                  'feedback_hit_smallwin' : feedback_hit_smallwin,
                  'feedback_hit_nowin' : feedback_hit_nowin,
                  'feedback_noresp' : feedback_noresp,
                  'press_left' : press_left,
                  'press_right' : press_right}
   """
    conditions['anticip_hit_largewin'] = anticip_hit_largewin
    conditions['anticip_hit_smallwin'] = anticip_hit_smallwin
    conditions['anticip_hit_nowin'] = anticip_hit_nowin
    conditions['anticip_noresp'] = anticip_noresp
    conditions['feedback_hit_largewin'] = feedback_hit_largewin
    conditions['feedback_hit_smallwin'] = feedback_hit_smallwin
    conditions['feedback_hit_nowin'] = feedback_hit_nowin
    conditions['feedback_noresp'] = feedback_noresp
    conditions['press_left'] = press_left
    conditions['press_right'] = press_right
    
    
   

    condition = []
    onset = []
    durations = []
    for c in conditions:
        condition += [c]*len(conditions[c])
        onset = np.hstack([onset, conditions[c]])
        if c[0] == 'a':
            durations += [anticip_duration]*len(conditions[c])
        elif c[0] == 'f':
            durations += [feedback_duration]*len(conditions[c])
        else:
            durations += [0]*len(conditions[c])

    paradigm = BlockParadigm(con_id=condition,
                             onset=onset,
                             duration=durations)
                               
    frametimes = np.linspace(0, (N_SCANS-1)*TR, num=N_SCANS)
    design_mat = design_matrix.make_dmtx(frametimes, paradigm,
                                     hrf_model='Canonical',
                                     drift_model='Cosine',
                                     hfcut=128)
                                     
    output_file = os.path.join(BASE_DIR, 'dev', 'playground', 'python',
                               'neuroimage', 'eprime', 'eprime_files',
                               'mat', f.split('/')[-1].split('.')[0])
    
    durations =  OrderedDict()
    durations = {'anticip_hit_largewin' : 4.,
                  'anticip_hit_smallwin' : 4.,
                  'anticip_hit_nowin' : 4.,
                  'anticip_missed_largewin' : 4.,
                  'anticip_missed_smallwin' : 4.,
                  'anticip_missed_nowin' : 4.,
                  'anticip_noresp' : 4.,
                  'feedback_hit_largewin' : 1.45,
                  'feedback_hit_smallwin' : 1.45,
                  'feedback_hit_nowin' : 1.45,
                  'feedback_missed_largewin' : 1.45,
                  'feedback_missed_smallwin' : 1.45,
                  'feedback_missed_nowin' : 1.45,
                  'feedback_noresp' : 1.45,
                  'press_left' : 0.,
                  'press_right' : 0.}

    generate_multiconditions_mat(output_file, conditions, durations)

    fig_title = f.split('/')[-1].split('.')[0]
    if len(subject_id)>0:
        fig_title += '-S'+ str(subject_id[0])
        output_file_s = os.path.join(BASE_DIR, 'dev', 'playground', 'python',
                               'neuroimage', 'eprime', 'eprime_files',
                               'mat', ''.join(['S',str(subject_id[0]),'_cond']))        
        generate_multiconditions_mat(output_file_s, conditions, durations)
    #design_mat.show()
    #plt.title(fig_title)
    
