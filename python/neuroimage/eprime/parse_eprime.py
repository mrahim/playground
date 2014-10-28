"""
A script for parsing e-prime files
:Author: RAHIM Mehdi
"""
import os
import numpy as np
import pandas as pd

# File id and date Parser
def eprime_parse_filename(filename):
    ''' returns the file_id and the corrected date from the filename '''
    file_id = filename.split('-')[1].strip()
    c_date = ''
    if len(file_id) == 5:
        c_date = file_id[2:4] + '-' + file_id[0:2]
        if file_id[4] < '9':
            c_date += '-201' + file_id[4]
        else:
            c_date += '-200' + file_id[4]
    return file_id, c_date

# Quick and Dirty Parser
def eprime_parse_data(filename):
    ''' returns a dict of the header and a DataFrame of values
    in the 3rd level of the given file '''
    edf = pd.DataFrame() # Subject dataframe
    lvl = {}    # E-Prime level 3 dict
    hdr = {} # Header dict
    level_flag = -1 # Flag on the current header/level
    with open(filename, 'rU') as f:
        lines = [x.strip() for x in f.read().split('\n')]
        for line in lines:
            if line in ["*** Header Start ***", "*** Header End ***"]:
                # set the flag on header section
                level_flag = 0
                continue
            if line == "*** LogFrame Start ***":
                # reset the level 3 dict
                lvl = {}
                continue
            if line == "*** LogFrame End ***":
                # append dict according to the level
                if lvl:
                    edf = edf.append(lvl, ignore_index=True)
                level_flag = -1
                continue
            fields = line.split(": ")
            fields[0] = fields[0].replace(':', '')
            fields[0] = fields[0].replace(' ', '')
            if fields[0] == "Level":
                level_flag = int(fields[1])
                continue
            if level_flag == 3:
                lvl[fields[0]] = ''
                if len(fields) == 2:
                    lvl[fields[0]] = fields[1]
            elif level_flag in [0, 1, 2]:
                hdr[fields[0]] = fields[1]
    return edf, hdr

'''
Parsing all subjects and saving :
    - a session csv per subject 
    - a whole subject header csv 
'''
header_selected_cols = ['c_Subject', 'Subject', 'c_SessionDate',
                        'SessionDate', 'SessionTime', 'nbTrials', 'PP.Onset']
eprime_selected_cols = ['TrialList',
                        'PictureTarget.OnsetTime',
                        'PictureTarget.ACC',
                        'SumPrize',
                        'prize',
                        'CorrectAnswer',
                        'PictureTarget.CRESP',
                        'PictureTarget.RESP',
                        'PictureTarget.OnsetDelay',
                        'PictureTarget.RT',
                        'PictureTarget.RTTime',
                        'TargetPosition',
                        'Target_time',
                        'Ant_time',
                        'Fix_time',
                        'J_time',
                        'PicturePrime.OnsetTime',
                        'PicturePrime.OnsetDelay']
header = pd.DataFrame()
for fn in os.listdir('eprime_files'):
    if(fn[0] == 'M'):
        print fn
        df, hd = eprime_parse_data(os.path.join('eprime_files', fn))
        hd['PP.Onset'] = ''
        if 'PicturePrime.OnsetTime' in df.keys():
            hd['PP.Onset'] = df['PicturePrime.OnsetTime'][0]
        hd['c_Subject'], hd['c_SessionDate'] = eprime_parse_filename(fn)
        hd['nbTrials'] = np.str(df['TrialList'].count())
        header = header.append(hd, ignore_index=True)
        # Save subject sessions
        df.to_csv(os.path.join('eprime_files', 'csv',
                               os.path.splitext(fn)[0] + '.csv'), sep=',')
        if hd['nbTrials'] == '66':
            df.to_csv(os.path.join('eprime_files', 'csv',
                               'c_' + os.path.splitext(fn)[0] + '.csv'), 
                                sep=',', columns=eprime_selected_cols)
# Save all subjects metadata
header.to_csv(os.path.join('eprime_files', 'csv', 'all_subjects.csv'),
              sep=',')
header.to_csv(os.path.join('eprime_files', 'csv', 'all_subjects_c.csv'),
              sep=',', columns=header_selected_cols)
