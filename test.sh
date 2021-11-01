#!/bin/bash
#module load FreeSurfer/6.0.0
#module load FSL
export SUBJECTS_DIR=/opt/freesurfer/subjects
declare -a subject=("010042")
dir=/home/yvonne/PycharmProjects/pythonProject/GCCA/data
for sub in "${subject[@]}"
do for scan in _ses-02_task-rest_acq-AP_run-1 _ses-02_task-rest_acq-AP_run-2
do for hemi in lh rh
do mri_vol2surf --mov ${dir}/sub-"$sub"/ses-02/func/sub-"$sub"${scan}_space-MNI152NLin6Asym_desc-smoothAROMAnonaggr_boldscaled.nii.gz\
  --mni152reg \
  --projfrac-avg 0.2 0.8 0.1 \
  --trgsubject fsaverage5 \
  --interp nearest \
  --hemi ${hemi} \
  --surf-fwhm 12.0 --cortex --noreshape \
  --o ${dir}/sub-"$sub"/sendToDaniel/sub-"$sub"${scan}-smoothAROMAnonaggr_boldscaled.fsa5.${hemi}.mgz 
done
done
done
