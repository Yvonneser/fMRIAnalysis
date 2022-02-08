"""
Import Packages
"""
import numpy as np
import nibabel as nib
from mvlearn.embed import GCCA
from nilearn.plotting import plot_surf_stat_map
import matplotlib.colors as colors
from matplotlib import pyplot as plt


"""
Build our color map  
"""
first = int((128 * 2) - np.round(255 * (1. - 0.65)))
second = (256 - first)
colors2 = plt.cm.viridis(np.linspace(0.1, .65, first))
colors3 = plt.cm.YlOrBr(np.linspace(0.5, 1., second))
colors1 = plt.cm.viridis(np.linspace(0., .98, first))
colors4 = plt.cm.YlOrBr(np.linspace(0.3, 0.90, second))

# combine them and build a new colormap
cols1 = np.vstack((colors2, colors3))
cols2 = np.vstack((colors1, colors4))

mymap1 = colors.LinearSegmentedColormap.from_list('my_colormap1', cols1)

num = 256
gradient = range(num)
for x in range(5):
    gradient = np.vstack((gradient, gradient))

fig, ax = plt.subplots(nrows=1)
ax.imshow(gradient, cmap=mymap1, interpolation='nearest')
ax.set_axis_off()
fig.tight_layout()

plt.show()

mymap2 = colors.LinearSegmentedColormap.from_list('my_colormap2', cols2)

num = 256
gradient = range(num)
for x in range(5):
    gradient = np.vstack((gradient, gradient))

fig, ax = plt.subplots(nrows=1)
ax.imshow(gradient, cmap=mymap2, interpolation='nearest')
ax.set_axis_off()
fig.tight_layout()

plt.show()


"""
load surfaces and cortex label
"""
surf_lh = nib.freesurfer.read_geometry('fsaverage5/surf/lh.inflated')
surf_rh = nib.freesurfer.read_geometry('fsaverage5/surf/rh.inflated')

cort_lh = nib.freesurfer.read_label('fsaverage5/label/lh.cortex.label')
cort_rh = nib.freesurfer.read_label('fsaverage5/label/rh.cortex.label')
cort = np.concatenate((cort_lh, cort_rh + 10242))

"""
load subject timeseries
Example data available for nine subjects here:
https://www.dropbox.com/sh/rotu9742d5vkm18/AACmfzJDajKEzxgzPDZ-ysEda?dl=0

As in example above, data should be loaded as single array of nodes x time points
already preprocessed, spatially smoothed (note that example data hasn't been smoothed),
and with nuisance regresssion (but without global signal regression)
"""

data = []
subjs = ['0025441','0025442','0025443','0025444','0025445','0025446','0025447','0025448','0025449']
ses = ["ses-01","ses-02","ses-10"]
for se in ses:
    for s in subjs:
        data.append(np.load('ts_HNG_data/ts_%s-%s_smoth12.npy' % (s ,se))[cort,])
    print(np.shape(data))


# RUN GCCA
gcca = GCCA(n_components=5)
"""
 or specify another thresholding eg, n_components=5 or fraction_var=0.8
 Still not sure about that parameter selection
"""
gcca.fit(data)
projs = gcca.transform(data)
print(np.shape(projs))
#np.save('pca_results.npy', projs)


"""
set visualization parameters:
"""

n_comps = np.shape(projs)[1]
if n_comps > 5:  # set max number of components to show at 5
    n_comps = 5

n_subs = 1

n_views = 4  # number of brains to show per component
fig_width = 10

""" 
Visualize group-level average components 
"""
fig = plt.figure(figsize=(fig_width, fig_width * n_comps * 0.25), dpi=400)
for component in range(n_comps):
    ax1 = fig.add_subplot(n_comps, n_views, component * n_views + 1, projection='3d')
    ax2 = fig.add_subplot(n_comps, n_views, component * n_views + 2, projection='3d')
    ax3 = fig.add_subplot(n_comps, n_views, component * n_views + 3, projection='3d')
    ax4 = fig.add_subplot(n_comps, n_views, component * n_views + 4, projection='3d')
    res = np.zeros(10242)
    res[cort_lh] = np.mean(np.asarray(projs)[:, :len(cort_lh), component], axis=0)
    plax1 = plot_surf_stat_map(surf_lh, res, hemi='left', view='medial', axes=ax1, colorbar=False, cmap=mymap1)
    plax2 = plot_surf_stat_map(surf_lh, res, hemi='left', view='lateral', axes=ax2, colorbar=False, cmap=mymap1)
    res = np.zeros(10242)
    res[cort_rh] = np.mean(np.asarray(projs)[:, len(cort_lh):, component], axis=0)

    plax3 = plot_surf_stat_map(surf_rh, res, hemi='right', view='lateral', axes=ax3, colorbar=False, cmap=mymap1)
    plax4 = plot_surf_stat_map(surf_rh, res, hemi='right', view='medial', axes=ax4, colorbar=False, cmap=mymap1)
    plt.figtext(0.5, 0.96 - (1. / n_comps) * component, 'G %i' % int(int(component) + 1),
                horizontalalignment='center', fontsize='large',fontweight='bold')

plt.tight_layout()
plt.subplots_adjust(hspace=0.1,wspace=0.05)
filename = 'HNG_Group_GCCA_all_ses_smoth12.png'
plt.savefig(filename, dpi=400)
plt.show()
