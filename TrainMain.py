import numpy as np
import cv2
import pickle
import DataProcessor
import EmotionLearner
from sklearn import svm
import matplotlib.pyplot as plt

dataProcessor=DataProcessor()
data,label=dataProcessor.loadCKData_With_Hog_32x32_3x3()
data,featureMeans,featureVariance=dataProcessor.normalizeData(data)

emotionLearner=EmotionLearner()
scores=emotionLearner.crossValidateSVM(data,label);
print scores
print np.means(scores)
clf=emotionLearner.trainSVM(data,label);

#save data and svm
with open('classifier/trainingDataCK.pkl', 'wb') as output:
    pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
    pickle.dump(label, output, pickle.HIGHEST_PROTOCOL)
    pickle.dump(featureMeans, output, pickle.HIGHEST_PROTOCOL)
    pickle.dump(featureVariance, output, pickle.HIGHEST_PROTOCOL)

with open('classifier/svmCK.pkl', 'wb') as output:
    pickle.dump(clf, output, pickle.HIGHEST_PROTOCOL)