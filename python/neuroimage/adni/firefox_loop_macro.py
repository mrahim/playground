# -*- coding: utf-8 -*-
"""
Generate iim file (iMacros) for Firefox
It contains a script which fills a IDA query result of ADNI
and save it in a collection
@author: mehdi
"""
import numpy as np

query_1 = 'TAB T=1\nURL GOTO=https://ida.loni.usc.edu/ladvq_results.jsp?mode=later&pageNum='
number = '2'
query_2 = '&project=ADNI&image_type_description=Original\nTAG POS=1 TYPE=INPUT:CHECKBOX FORM=NAME:resultForm ATTR=NAME:selectAll CONTENT=YES\nTAG POS=1 TYPE=INPUT:IMAGE ATTR=ID:add\nTAG POS=1 TYPE=SELECT FORM=NAME:addCollection ATTR=NAME:existingCollections CONTENT=%63893\nTAG POS=1 TYPE=IMG ATTR=ID:submit1'

long_string= ('qsdf'
              'qsdf '
              ' sdfqsdf sdf qsdf qsdf ')

query_full = 'VERSION BUILD=8820413 RECORDER=FX\n'
for number in np.arange(2, 73):
    query_full += query_1+str(number)+query_2+'\n\n'

print query_full

text_file = open("myrequest.iim", "w+")
text_file.write(query_full)
text_file.close()