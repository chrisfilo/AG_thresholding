'''
Created on 22 Oct 2010

@author: filo
'''
import nipype.externals.pynifti as nb
import numpy as np
from scipy.ndimage.morphology import binary_erosion
from scipy.ndimage.measurements import center_of_mass, label
from scipy.spatial.distance import cdist, euclidean
import matplotlib
matplotlib.use('Cairo')
import matplotlib.pyplot as plt

image_filename1 = '/media/sdb2/laura_study/workdir/compare_pipeline/_subject_id_AG_1247/reslice_tumour/rtumour.nii'
#image_filename2 = '/media/sdb2/laura_study/workdir/compare_pipeline/_subject_id_AG_1247/expert_flip/rAG_1247_LHclench_t10_out.nii'
image_filename2 = "/media/sdb2/laura_study/workdir/compare_pipeline/_subject_id_AG_1247/expert_fix_affine/fAG_1247_LHclench_t10_transformed.nii"

def findBorder(data):
    eroded = binary_erosion(data)
    border = np.logical_and(data, np.logical_not(eroded))
    return border

def getCoordinates(data, affine):
    if len(data.shape) == 4:
        data = data[:,:,:,0]
    indices = np.vstack(np.nonzero(data))
    indices = np.vstack((indices, np.ones(indices.shape[1])))
    coordinates = np.dot(affine,indices)
    return coordinates[:3,:]

nii1 = nb.load(image_filename1)
origdata1 = nii1.get_data().astype(np.bool)

#cog_t = np.array(center_of_mass(origdata1)).reshape(-1,1)
#cog_t = np.vstack((cog_t, np.array([1])))
#
#print cog_t.shape
#
#cog_t_coor = np.dot(nii1.get_affine(),cog_t)[:3,:]
#
#nii2 = nb.load(image_filename2)
#origdata2 = nii2.get_data().astype(np.bool)
#(labeled_data, n_labels) = label(origdata2)
#
#cogs = np.ones((4,n_labels))
#
#for i in range(n_labels):
#    cogs[:3,i] = np.array(center_of_mass(origdata2, labeled_data, i+1))
#    
#cogs_coor = np.dot(nii2.get_affine(),cogs)[:3,:]
#print cogs_coor
#
#dist_matrix = cdist(cog_t_coor.T, cogs_coor.T)
#print dist_matrix
#
#mean_dist = np.mean(dist_matrix)
#
#print mean_dist








border1 = findBorder(origdata1)
print np.sum(border1)

nb.save(nb.Nifti1Image(border1, nii1.get_affine(), nii1.get_header()), "border1.nii")

nii2 = nb.load(image_filename2)
origdata2 = nii2.get_data().astype(np.bool)
border2 = findBorder(origdata2)
print np.sum(border2)
nb.save(nb.Nifti1Image(border2, nii2.get_affine(), nii2.get_header()), "border2.nii")

set1_coordinates = getCoordinates(border1, nii1.get_affine())
print set1_coordinates.T.shape

set2_coordinates = getCoordinates(origdata2, nii2.get_affine())
print set2_coordinates.T.shape

dist_matrix = cdist(set1_coordinates.T, set2_coordinates.T)
print dist_matrix.shape
min_dist_matrix = np.amin(dist_matrix, axis = 0)
print min_dist_matrix.shape

print np.average(min_dist_matrix, weights=nii2.get_data()[origdata2].flat)
print np.mean(min_dist_matrix)
print np.min(min_dist_matrix)

plt.hist(min_dist_matrix, 50, normed=1, facecolor='green')
plt.savefig("hist.pdf")

#count = 0
#for point in set1_indices:
#    for point in set1_indices:
#        count+=1
#        print count