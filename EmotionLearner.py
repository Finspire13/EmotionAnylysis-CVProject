import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn import svm

class EmotionLearner:
    def trainSVM(self,data,label):
        clf = svm.SVC(decision_function_shape='ovo',probability=True)
        clf.fit(data,label)
        return clf
    def crossValidateSVM(self,data,label):
        clf = svm.SVC(decision_function_shape='ovo',probability=True)
        scores = cross_val_score(clf, data, label)
        return scores