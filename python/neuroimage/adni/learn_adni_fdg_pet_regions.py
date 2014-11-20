"""
A script that :
- extracts regions from FDG PET (baseline uniform)
- cross-validates a linear SVM classifier
- computes a ROC curve and AUC
"""

import os, glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import nibabel as nib
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc

def plot_groups(data):
    """Cumulative bars of pairwise groups
    """
    groups = data.groupby('DX_Group').size()
    labels = ['AD/Normal', 'AD/MCI', 'MCI/Normal', 'MCI/LMCI']
    
    p1 = [groups.AD, groups.AD, groups.MCI, groups.MCI]
    p2 = [groups.Normal, groups.MCI, groups.Normal, groups.LMCI]
    width = .35
    plt.bar(range(len(p1)), p1, width, color='g')    
    plt.bar(range(len(p2)), p2, width, color='y', bottom=p1)
    plt.ylabel('Individuals')
    plt.title('Population repartition')
    plt.xticks(np.arange(len(p1))+width/2., labels )
    plt.yticks(np.arange(0,81,10))
    fname = 'population_repartition_adni_baseline'
    plt.savefig(os.path.join('figures', fname))


def plot_shufflesplit(score, pairwise_groups):
    """Boxplot of the accuracies
    """
    bp = plt.boxplot(score, labels=['/'.join(pg) for pg in pairwise_groups])
    for key in bp.keys():
        for box in bp[key]:
            box.set(linewidth=2)
    plt.grid(axis='y')
    plt.ylabel('Accuracy')
    plt.title('ADNI baseline accuracies (regions)')
    plt.legend(loc="lower right")
    for ext in ['png', 'pdf', 'svg']:
        fname = '.'.join(['boxplot_adni_baseline_regions_norm', ext])
        plt.savefig(os.path.join('figures', fname))


def plot_roc(cv_dict):
    """Plot roc curves for each pairwise groupe
    """
    for pg in cv_dict.keys():
        plt.plot(crossval[pg]['fpr'],crossval[pg]['tpr'],
                 linewidth=2,
                 label='{0} (auc = {1:0.2f})'
                                   ''.format(pg, crossval[pg]['auc']))
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.grid(True)
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ADNI baseline ROC curves (regions)')
        plt.legend(loc="lower right")
    
    for ext in ['png', 'pdf', 'svg']:
        fname = '.'.join(['roc_adni_baseline_regions_norm', ext])
        plt.savefig(os.path.join('figures', fname))



BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'
data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))
Y = np.zeros(len(data))
Y[data[data.DX_Group=='AD'].index.values]=1

if os.path.exists('features_regions.npy'):
    X = np.load('features_regions.npy')
else:
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
                X[idx,(val/256)-1] = np.mean(pet_data[ind])
    np.save('features_regions', X)

    pet_data = pet_img.get_data()
    seg_data = seg_img.get_data()[:, :, :, 0]
    
    for val in np.unique(seg_data):
        if val > 0:
            ind = (seg_data == val)
            X[idx,(val/256)-1] = np.mean(pet_data[ind])

#AD/MCI, AD/Normal, MCI/LMCI, MCI/Normal
pairwise_groups = [['AD', 'Normal'],
                   ['AD', 'MCI'],
                   ['MCI', 'Normal'],
                   ['MCI', 'LMCI']]
nb_iter = 100
score = np.zeros((nb_iter, len(pairwise_groups)))
crossval = dict()
pg_counter = 0
for pg in pairwise_groups:
    x = np.zeros([0,83])
    for dx in pg:
        print dx
        ind = data[data.DX_Group == dx].index.values
        x = np.append(x, X[ind,:], axis=0)
    y = np.ones(len(x))
    y[len(y) - len(ind):] = 0

    
    estim = svm.SVC(kernel='linear')
    sss = cross_validation.StratifiedShuffleSplit(y, n_iter=nb_iter, test_size=0.25)
    # 1000 runs with randoms 75% / 25% : StratifiedShuffleSplit
    counter = 0
    for train, test in sss:
        Xtrain, Xtest = x[train], x[test]
        Ytrain, Ytest = y[train], y[test]
        Yscore = estim.fit(Xtrain,Ytrain)
        print pg_counter, counter
        score[counter, pg_counter] = estim.score(Xtest, Ytest)
        counter += 1

    # Cross-validation
    kf = cross_validation.StratifiedKFold(y,4)
    estim = svm.SVC(kernel='linear', probability=True)
    yproba = np.zeros((len(y), 2))
    
    for train, test in kf:
        xtrain, xtest = x[train], x[test]
        ytrain, ytest = y[train], y[test]
        yproba[test] = estim.fit(xtrain, ytrain).predict_proba(xtest)
        
    fpr, tpr, thresholds = roc_curve(1-y, yproba[:,0])
    a = auc(fpr,tpr)
    if a<.5:
        fpr, tpr, thresholds = roc_curve(y, yproba[:,0])
        a = auc(fpr,tpr)
    crossval['/'.join(pg)] = {'fpr' : fpr,
                              'tpr' : tpr,
                              'thresholds' : thresholds,
                              'yproba' : yproba,
                              'auc' : a}
    pg_counter += 1

plot_roc(crossval)
plt.figure()
plot_shufflesplit(score, pairwise_groups)
plt.figure()
