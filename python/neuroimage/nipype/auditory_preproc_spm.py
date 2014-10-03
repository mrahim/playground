# -*- coding: utf-8 -*-
"""
Auditory fMRI pre-processing with spm via nipype
"""

import os
import numpy as np
import nipype.interfaces.spm as spm
import nipype.pipeline.engine as pe
import nipype.algorithms.modelgen as model

# Global paths
BASE_DIR = '/volatile/accounts/mehdi/data/examples/MoAEpilot/'
MATLAB_CMD = '/usr/local/bin/spm12b run script'

# SPM configuration
spm.SPMCommand.set_mlab_paths(matlab_cmd=MATLAB_CMD, use_mcr=True)

# Realignment
realigner = pe.Node(interface=spm.Realign(), name='realignment')
realigner.inputs.in_files = os.path.join(BASE_DIR, 'fM00223', 'fM00223.nii')
realigner.inputs.register_to_mean =  True

# Coregistration
coregister = pe.Node(interface=spm.Coregister(), name='coregistration')
coregister.inputs.source = os.path.join(BASE_DIR, 'sM00223', 'sM00223.nii')

# Segmentation
segmenter = pe.Node(interface=spm.Segment(), name='segmentation')
segmenter.inputs.save_bias_corrected = True

# Normalization
normalizer_s = pe.Node(interface=spm.Normalize(), name='normalization_s')
normalizer_s.inputs.jobtype = 'write'

normalizer_f = pe.Node(interface=spm.Normalize(), name='normalization_f')
normalizer_f.inputs.jobtype = 'write'

# Smoothing
smoother = pe.Node(interface=spm.Smooth(), name='smoothing')
smoother.inputs.fwhm = [4, 4, 4]
smoother.inputs.in_files = os.path.join(BASE_DIR, 'sM00223', 'sM00223.nii')

# Pipeline specification
preproc = pe.Workflow(name='preprocessing')
preproc.base_dir = os.path.join(BASE_DIR)
preproc.connect([(realigner, coregister, [('mean_image', 'target')]),
                  (coregister, segmenter, [('coregistered_source','data')]),
(segmenter, normalizer_s, [('transformation_mat','parameter_file')]),
(segmenter, normalizer_s, [('bias_corrected_image','source')]),
(segmenter, normalizer_f, [('transformation_mat','parameter_file')]),
(realigner, normalizer_f, [('realigned_files','source')])
])
preproc.run()
preproc.write_graph()