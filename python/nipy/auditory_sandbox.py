# -*- coding: utf-8 -*-
"""
Auditory fMRI first level analysis with spm via nipype
"""

import os
import numpy as np
import nipype.interfaces.spm as spm
import nipype.pipeline.engine as pe
import nipype.algorithms.modelgen as model
from nipype.interfaces.base import Bunch

# Global paths
BASE_DIR = '/volatile/accounts/mehdi/data/examples/MoAEpilot/'
MATLAB_CMD = '/usr/local/bin/spm12b run script'

# SPM configuration
spm.SPMCommand.set_mlab_paths(matlab_cmd=MATLAB_CMD, use_mcr=True)


# 1st level analysis
# Model specification
modelspec = pe.Node(interface=model.SpecifySPMModel(),
                    name='model_specification')
modelspec.inputs.input_units = 'secs'
modelspec.inputs.time_repetition = 7.
modelspec.inputs.high_pass_filter_cutoff = 168.
modelspec.inputs.functional_runs = [os.path.join( BASE_DIR, 'fM00223',
                         '4D_preproc.nii')]
subject_info = Bunch(conditions=['Listen'],
                     onsets=[7. * np.arange(6,84,12)],
                     durations=[[42.]])                     
modelspec.inputs.subject_info = subject_info
modelspec.base_dir = os.path.join(BASE_DIR,'analysis')
modelspec.run()


# Design
lvl1design = pe.Node(interface=spm.Level1Design(), name='model_design')
lvl1design.inputs.session_info = modelspec.get_output('session_info')
lvl1design.inputs.interscan_interval = 7.
lvl1design.inputs.timing_units = 'secs'
lvl1design.inputs.bases = {'hrf':{}}
lvl1design.base_dir = os.path.join(BASE_DIR,'analysis')
lvl1design.run()


# Model estimation
lvl1estimate = pe.Node(interface=spm.EstimateModel(),
                       name='model_estimation')
lvl1estimate.inputs.estimation_method = {'Classical':{}}
lvl1estimate.inputs.spm_mat_file = lvl1design.get_output('spm_mat_file')
lvl1estimate.base_dir = os.path.join(BASE_DIR,'analysis')
lvl1estimate.run()
