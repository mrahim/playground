"""
A script for parsing e-prime files
:Author: RAHIM Mehdi
"""
import os
import pandas as pd

# File ID Parsing Function
def eprime_parse_filename(filename):
    ''' returns the file_id of from the filename '''
    return filename.split('-')[1]

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


''' Parsing all subjects and saving :
- a session csv per subject
- a whole subject header csv '''
header = pd.DataFrame()
for fn in os.listdir('eprime_files'):
    if(fn[0] == 'M'):
        df, hd = eprime_parse_data(os.path.join('eprime_files', fn))
        df.to_csv(os.path.join('eprime_files','csv',
                               os.path.splitext(fn)[0]+'.csv'), sep=',')
        header = header.append(hd, ignore_index=True)
header.to_csv(os.path.join('eprime_files','csv','all_subjects.csv'), sep=',')        
