import os
import numpy as np
import cv2
from skimage.feature import hog
class DataProcessor:
    def loadCKData_With_Hog_32x32_3x3(self):
        #prepare training data. feature extraction
        label=[]
        data=[]

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml') 

        probe=0
        for subDir in os.listdir('data/ckLabel'):
            if subDir!=".DS_Store":
                for shotDir in os.listdir('data/ckLabel/'+subDir):
                    if shotDir!=".DS_Store":
                        for labelName in os.listdir('data/ckLabel/'+subDir+'/'+shotDir):
                            if labelName!=".DS_Store":
                                labelPath='data/ckLabel/'+subDir+'/'+shotDir+'/'+labelName
                                labelFile=open(labelPath)
                                for line in labelFile:
                                    tempLabel=float(line.lstrip())
                                
                                imageList=os.listdir('data/ck/'+subDir+'/'+shotDir)
                                acceptableNum=int(len(imageList)/2)
                                neutralNum=int(len(imageList)/6)
                                neutralNum=min(neutralNum,2)
                        
                                for imageName in imageList[acceptableNum:]:
                                    imagePath='data/ck/'+subDir+'/'+shotDir+'/'+imageName
                                    image = cv2.imread(imagePath)
                                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                    for (x,y,w,h) in faces:
                                        roi_gray = gray[y:y+h, x:x+w]
                                        roi_gray = cv2.resize(roi_gray,(256, 256), interpolation = cv2.INTER_CUBIC)
                                    
                                        #imageFeatures=[]
                                        #for i in range(2):
                                        #    for j in range(2)
                                        #        patch=roi_gray[i*128:(i+1)*128,j*128:(j+1)*128]
                                        #        fd, hog_image = hog(patch, orientations=8, pixels_per_cell=(32, 32),cells_per_block=(3, 3), visualise=True)
                                        #        imageFeatures.extend(fd)
                                        imageFeatures, hog_image = hog(roi_gray, orientations=8, pixels_per_cell=(32, 32),cells_per_block=(3, 3), visualise=True)
                            
                                
                                        data.append(imageFeatures)
                                        label.append(tempLabel)
                                        probe+=1
                                        print probe
                        
                                for imageName in imageList[:neutralNum]:
                                    if imageName!=".DS_Store":
                                        imagePath='data/ck/'+subDir+'/'+shotDir+'/'+imageName
                                        image = cv2.imread(imagePath)
                                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                                        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                        for (x,y,w,h) in faces:
                                            roi_gray = gray[y:y+h, x:x+w]
                                            roi_gray = cv2.resize(roi_gray,(256, 256), interpolation = cv2.INTER_CUBIC)
                            
                                            #imageFeatures=[]
                                            #for i in range(2):
                                            #    for j in range(2)
                                            #        patch=roi_gray[i*128:(i+1)*128,j*128:(j+1)*128]
                                            #        fd, hog_image = hog(patch, orientations=8, pixels_per_cell=(32, 32),cells_per_block=(3, 3), visualise=True)
                                            #        imageFeatures.extend(fd)
                                            imageFeatures, hog_image = hog(roi_gray, orientations=8, pixels_per_cell=(32, 32),cells_per_block=(3, 3), visualise=True)
                            
                                            data.append(imageFeatures)
                                            label.append(0.0)
                                            probe+=1
                                            print probe
        
        data=np.array(data)
        label=np.array(label)
        return data,label   
    
    def normalizeData(self,data):
        featureMeans=[]
        featureVariance=[]
        for i in range(data.shape[1]):
            feature=data[:,i]
            tempMean=np.mean(feature)
            feature-=tempMean
            featureMeans.append(tempMean)
    
            tempVariance=np.sqrt(np.var(feature))
            if tempVariance!=0:
                feature/=tempVariance
            else:
                print "zero var"
            featureVariance.append(tempVariance)
    
            data[:,i]=feature
    
        featureMeans=np.array(featureMeans)
        featureVariance=np.array(featureVariance)

        #pca = PCA(n_components=200)
        #pca.fit(data)
        #newData=pca.fit_transform(data)

        #print np.array(newData).shape
        #print newData
        
        return data,featureMeans,featureVariance