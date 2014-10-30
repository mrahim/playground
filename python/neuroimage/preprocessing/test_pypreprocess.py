"""
Test
"""
import os, glob
from pypreprocess.nipype_preproc_spm_utils import do_subject_preproc
from pypreprocess.subject_data import SubjectData
from nilearn import plotting, image

BASE_DIR = os.path.join('/', 'shfj', 'Ppsypim', 'PSYDAT', 'Subjects')
OUPUT_DIR = os.path.join('/', 'disk4t', 'mehdi', 'data', 'psydat')

subject_list = os.listdir(BASE_DIR)

for subject_id in subject_list:
    # fMRI
    fmri_path = os.path.join(BASE_DIR, subject_id, 'MRI', 'MID')
    fmri_list = glob.glob(os.path.join(fmri_path, '[E-S]*.nii'))

    # MRI        
    anat_path = os.path.join(BASE_DIR, subject_id, 'MRI', 'T1MRI')
    anat_list = glob.glob(os.path.join(anat_path, '[E-n]*.hdr'))
    
    if len(fmri_list) == 291 and len(anat_list) == 1 and subject_id != 'S14659':
        print subject_id, len(anat_list), len(fmri_list)

        subject_data = SubjectData(func=[fmri_list[2:]],
                                   anat=anat_list[0],
                                   output_dir=os.path.join(OUPUT_DIR,
                                   subject_id))
                                   
        
        anat_name = '_'.join([subject_id, 'anat'])
        r_img_anat = image.reorder_img(anat_list[0], resample=True)
        
        plotting.plot_img(r_img_anat,
                          output_file=os.path.join(OUPUT_DIR, 'figs', anat_name),
                          title=anat_name,
                          black_bg=True)
        #############################################
        do_subject_preproc(
            subject_data, #subject data class
            deleteorient=False, #
        
            slice_timing=True,
            slice_order="ascending",
            interleaved=True,
            refslice=1,
            TR=2.4,
            TA=2.3,
            slice_timing_software="spm",
        
            realign=True,
            realign_reslice=False,
            register_to_mean=True,
            realign_software="spm",
        
            coregister=True,
            coregister_reslice=False,
            coreg_anat_to_func=True,
            coregister_software="spm",
        
            segment=False,
        
            normalize=True,
            dartel=False,
            fwhm=3.,
            anat_fwhm=0.,
            func_write_voxel_sizes=3.,
            anat_write_voxel_sizes=1.,
        
            hardlink_output=True,
            report=True,
            cv_tc=True,
            parent_results_gallery=None,
            last_stage=True,
            preproc_undergone=None,
            prepreproc_undergone="",
            generate_preproc_undergone=True,
            caching=True,
            )

