# -*- coding: utf-8 -*-
"""
Parsing all subjects header
@author: mehdi
"""

import os

# Header Parsing Function
def eprime_parse_header(filename):
    ''' returns a dictionary of values in the header of the given file '''
    header = {}
    with open(filename, 'rU') as f:
        lines = [x.strip() for x in f.read().split('\n')]
        for line in lines:
            if line == "*** Header Start ***":
                continue
            if line == "*** Header End ***":
                return header
            fields = line.split(": ")
            if len(fields) == 2:
                header[fields[0]] = fields[1]

# File ID Parsing Function
def eprime_parse_filename(filename):
    ''' returns the file_id of from the filename '''
    return filename.split('-')[1]

# Header Parsing for all subjects
for fn in os.listdir('eprime_files'):
    if(fn[0] == 'M'):
        head = eprime_parse_header(os.path.join('eprime_files', fn))
        print head['SessionDate'], '-', head['SessionTime']
        print head['Subject'].strip(), '-', eprime_parse_filename(fn), '-', fn

