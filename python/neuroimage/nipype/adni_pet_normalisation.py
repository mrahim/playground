# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 09:29:19 2014

@author: mr243268
"""

import nipype.interfaces.spm as spm

norm = spm.Normalize()
norm.inputs.source = 'I26671.nii'
norm.inputs.template = 'PET.nii'
norm.inputs.paths = '/i2bm/local/spm8'
norm.run()