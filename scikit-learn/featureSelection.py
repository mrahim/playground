"""
    Testing scikit-learn features :
        - Feature selection
        Author : Mehdi Rahim
"""

print(__doc__)

import numpy as np
#import pylab as pl
from sklearn import svm
from scipy import io
from sklearn import cross_validation
#from sklearn.metrics import roc_curve, auc
from sklearn import feature_selection

Data = io.matlab.loadmat('../../../data/featuresLBP1097.mat')

X = Data['X'].T
y = np.ravel(Data['Y'])

svc = svm.SVC(kernel='linear')
rfe_cv = feature_selection.RFECV(svc,step=0.25,cv=cross_validation.StratifiedKFold(y,10),scoring='accuracy')
rfe_cv.fit(X,y)
print("Optimal number of features : %d" % rfe_cv.n_features_)