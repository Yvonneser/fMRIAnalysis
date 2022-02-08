import os
import subprocess

import load_confounds as lc
from nilearn.input_data import NiftiMasker
import nibabel as nib

#Function to set TR prameter in the NiftiIMAGE
def set_tr(img, tr):
    header = img.header.copy()
    zooms = header.get_zooms()[:3] + (tr,)
    header.set_zooms(zooms)
    return img.__class__(img.get_fdata().copy(), img.affine, header)

subjs = ['0025441','0025442','0025443','0025444']
ses = ["ses-01","ses-02","ses-10"]
for se in ses:
    for s in subjs:
        # load_confounds auto-detects the companion .tsv file (which needs to be in the same directory)
        file = ("data/HNG-Data-fmriprep/derivative-%s/sub-%s/%s/func/sub-%s_%s_task-rest_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz" % (s,s ,se,s,se))
        confounds = lc.Minimal().load(file)
        RegImg = nib.load(file)
        # Use the confounds to load preprocessed time series with nilearn
        masker = NiftiMasker(smoothing_fwhm=6 ,standardize=True)
        img = masker.fit_transform(file, confounds=confounds)
        #transform and reshape the data
        img= masker.inverse_transform(img)
        img.header.set_xyzt_units("mm","sec")
        fixed_img = set_tr(img, RegImg.header.get_zooms()[3])
        nib.save(img, ('data/HNG-Data-fmriprep/derivative-%s/afterLoad%s/sub-%s_%s_MNI152NLin2009cAsym_desc-preproc_bold_afterLoadConf.nii.gz'% (s ,s,s,se)))


