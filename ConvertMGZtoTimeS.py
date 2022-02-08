### imports

import numpy as np
import nibabel as nib
from mvlearn.embed import GCCA
from nilearn.plotting import plot_surf_stat_map
import matplotlib.colors as colors
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

surf_lh = nib.freesurfer.read_geometry('fsaverage5/surf/lh.inflated')
surf_rh = nib.freesurfer.read_geometry('fsaverage5/surf/rh.inflated')

cort_lh = nib.freesurfer.read_label('fsaverage5/label/lh.cortex.label')
cort_rh = nib.freesurfer.read_label('fsaverage5/label/rh.cortex.label')
cortex = np.concatenate((cort_lh, cort_rh + 10242))



subjs = ['0025441','0025442','0025443','0025444','0025445','0025446','0025447','0025448','0025449']
ses = ["ses-01","ses-02","ses-10"]
for se in ses:
    for s in subjs:
        func_lh = (r'HNG-Data-fmriprep/aftervol2surf/sub-%s-%s-preproc_smoth12.fsa5.lh.mgz'%(s,se))
        func_rh = (r'HNG-Data-fmriprep/aftervol2surf/sub-%s-%s-preproc_smoth12.fsa5.rh.mgz'%(s,se))
        ts_lh = nib.load(func_lh).get_fdata().squeeze()
        ts_rh = nib.load(func_rh).get_fdata().squeeze()
        ts = np.vstack((ts_lh, ts_rh))
        np.save(('ts_HNG_data/ts_%s-%s_smoth12.npy' %(s,se)), ts)
