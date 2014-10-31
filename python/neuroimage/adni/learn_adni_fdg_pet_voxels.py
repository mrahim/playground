"""
A script that :
- extracts reg from FDG PET (baseline, uniform)
- reduces dimension and learn
"""

import os, glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import nibabel as nib
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc


BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'

data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))

Y = np.zeros(len(data))
Y[data[data.DX_Group=='AD'].index.values]=1

X = np.zeros((len(data), 83))
for idx, row in data.iterrows():
    pet_id = ''.join(['I', str(row['Image_ID_y'])])
    pet = glob.glob(os.path.join(BASE_DIR, pet_id, '*.nii.gz'))[0]
    
    seg_id = ''.join(['I', str(row['Image_ID_x'])])
    seg = glob.glob(os.path.join(BASE_DIR, seg_id, '*.nii'))[0]
    
    pet_img = nib.load(pet)
    seg_img = nib.load(seg)

    pet_data = pet_img.get_data()
    seg_data = seg_img.get_data()[:, :, :, 0]    
    
    for val in np.unique(seg_data):
        if val > 0:
            ind = (seg_data == val)
            X[idx,(val/256)-1] = np.std(pet_data[ind])



# Cross-validation
kf = cross_validation.StratifiedKFold(Y,5)
estim = svm.SVC(kernel='linear',probability=True,verbose=True)

Yscore = np.zeros((Y.size,2))

for train, test in kf:
    Xtrain = X[train]
    Ytrain = Y[train]
    Xtest  = X[test]
    Ytest  = Y[test]
    Yscore[test] = estim.fit(Xtrain,Ytrain).predict_proba(Xtest)
    
fpr, tpr, thresholds = roc_curve(1-Y,Yscore[:,0])
print auc(fpr,tpr)

plt.plot(fpr,tpr)
plt.xlim([0,1])
plt.ylim([0,1.05])
a=auc(fpr,tpr)
t = 'AUC = %.4f' % a
plt.title(t)
