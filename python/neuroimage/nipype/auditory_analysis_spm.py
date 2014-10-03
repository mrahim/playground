# -*- coding: utf-8 -*-
"""
Auditory fMRI pre-processing and first level analysis with spm via nipype
"""

import os
import numpy as np
import nipype.interfaces.spm as spm
import nipype.pipeline.engine as pe
import nipype.algorithms.modelgen as model
from nipype.interfaces.base import Bunch

from nipype import config
cfg = dict(logging=dict(workflow_level = 'DEBUG'),
           execution={'stop_on_first_crash': False,
                      'hash_method': 'content'})
config.update_config(cfg)

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
modelspec.inputs.functional_runs = [[os.path.join(BASE_DIR, 'fM00223',
                         '4D_preproc.nii')]]
modelspec.inputs.subject_info = Bunch(conditions=['Listen'],
                                      onsets=[7. * np.arange(6,84,12)],
durations=[[42.]])


# Level 1 design
lvl1design = pe.Node(interface=spm.Level1Design(), name='level1design')
lvl1design.inputs.interscan_interval = 7.
lvl1design.inputs.timing_units = 'secs'
lvl1design.inputs.bases = {'hrf':{}}

# Model estimation
lvl1estimate = pe.Node(interface=spm.EstimateModel(),
                       name='model_estimation')
lvl1estimate.inputs.estimation_method = {'Classical':{}}

# Workflow
analysis = pe.Workflow(name='analysis')
analysis.base_dir = BASE_DIR
analysis.connect([(modelspec, lvl1design, [('session_info', 'session_info')]),
                  (lvl1design, lvl1estimate, 
                   [('spm_mat_file', 'spm_mat_file')])])

analysis.run()
analysis.write_graph()