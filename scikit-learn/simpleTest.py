"""
    Testing scikit-learn features :
        - Basic I/O
        - SVM classification
        - ROC curves and Cross-Validation
        Author : Mehdi Rahim
"""

import numpy as np
import pylab as pl
from sklearn import svm
from sklearn.externals import joblib
from scipy import io
from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc

Data = io.matlab.loadmat('../../../data/featuresLBP1097.mat')

X = Data['X'].T
y = np.ravel(Data['Y'])


"""
estim = svm.LinearSVC()
S = estim.fit(X,y).score(X,y)

joblib.dump(estim,'diamela_classifier.pkl')
"""

# Cross-validation

kf = cross_validation.StratifiedKFold(y,10)
estim = svm.SVC(kernel='linear',probability=True,verbose=True)

Yscore = np.zeros((y.size,2))

for train, test in kf:
    Xtrain = X[train]
    Ytrain = y[train]
    Xtest  = X[test]
    Ytest  = y[test]       
    
    Yscore[test] = estim.fit(Xtrain,Ytrain).predict_proba(Xtest)
    

Y=y
Y[Y==2]=0
fpr, tpr, thresholds = roc_curve(Y,Yscore[:,0])
print auc(fpr,tpr)

pl.close('all')
pl.plot(fpr,tpr)
pl.xlim([0,1])
pl.ylim([0,1.05])
a=auc(fpr,tpr)
t = 'Skinan AUC = %.4f' % a
pl.title(t)

 
 
 