import numpy as np
import cv2
import pickle

#load data and svm
with open('classifier/trainingDataCK.pkl', 'rb') as input:
    data = pickle.load(input)
    label = pickle.load(input)
    featureMeans = pickle.load(input)
    featureVariance = pickle.load(input)
    print data.shape
    print label.shape
    print featureMeans.shape
    print featureVariance.shape
    
with open('classifier/svmCK.pkl', 'rb') as input:
    clf = pickle.load(input)
    
emotionPredictor=EmotionPredictor()
plotBuffer=emotionPredictor.startPredictionFromCamera(clf,featureMeans,featureVariance)

#frame=cv2.imread('data/ck/S999/003/S999_003_00000055.png')
#emotionPredictor.predictOneImage(clf,frame,featureMeans,featureVariance)
plotEmotions(plotBuffer)