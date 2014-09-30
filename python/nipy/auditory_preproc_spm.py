# -*- coding: utf-8 -*-
"""
Auditory fMRI pre-processing with spm via nipype
"""

import os

import nipype.interfaces.spm as spm
import nipype.pipeline.engine as pe

# Global paths
BASE_DIR = '/volatile/accounts/mehdi/data/examples/MoAEpilot/'
MATLAB_CMD = '/usr/local/bin/spm12b run script'

# SPM configuration
spm.SPMCommand.set_mlab_paths(matlab_cmd=MATLAB_CMD, use_mcr=True)


# Pipeline specification
realigner = pe.Node(interface=spm.Realign(), name='realign')
realigner.inputs.in_files = os.path.join(BASE_DIR, 'fM00223', 'fM00223.nii')
realigner.inputs.register_to_mean =  True

smoother = pe.Node(interface=spm.Smooth(), name='smooth')
smoother.inputs.fwhm = [4, 4, 4]

workflow = pe.Workflow(name='preproc')
workflow.base_dir = os.path.join(BASE_DIR)
workflow.connect(realigner, 'realigned_files', smoother, 'in_files')
workflow.run()
workflow.write_graph()
