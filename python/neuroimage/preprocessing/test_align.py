"""
Test
"""

import os
import glob
import matplotlib.pyplot as plt
from pypreprocess.reporting.check_preprocessing import plot_spm_motion_parameters
from pypreprocess.realign import MRIMotionCorrection


id_subject = 'S14847'

os.chdir("/shfj/Ppsypim/PSYDAT/Subjects/")
fmri_list = glob.glob(os.path.join(os.getcwd(),id_subject,'MRI','MID')+'/E*.nii')
fmri_list = fmri_list[3:]

mrimc = MRIMotionCorrection(n_sessions=289)
mrimc.fit(fmri_list)
realign = mrimc.transform('/disk4t/mehdi/data', reslice=True, concat=True)

for sess, rp_filename in zip(xrange(len(mrimc._rp_filenames_)),
                             mrimc._rp_filenames_):
    plot_spm_motion_parameters(
        rp_filename,
        title="Estimated motion")

plt.show()

