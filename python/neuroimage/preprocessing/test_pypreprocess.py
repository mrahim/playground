"""
Test
"""

import os
import glob
import matplotlib.pyplot as plt
from pypreprocess.reporting.check_preprocessing import plot_registration
from pypreprocess.coreg import Coregister


id_subject = 'S14817'

os.chdir("/home/Ppsypim/PSYDAT/Subjects/")

# fMRI
fmri_list = glob.glob(os.path.join(os.getcwd(),id_subject,'MRI','MID')+'/S*.nii')
fmri = fmri_list[5]

# MRI
mri_list = glob.glob(os.path.join(os.getcwd(),id_subject,'MRI','T1MRI')+'/*.img')
mri = mri_list[0]

output_dir = ''.join(['/home/mr243268/data/'])
                         
c = Coregister()
c.fit(fmri, mri)
new_img = c.transform(mri, output_dir=output_dir, prefix="ppr")

# QA
plot_registration(mri, fmri, title="before coreg")
plot_registration(new_img, fmri, title="after coreg")
plt.show()
