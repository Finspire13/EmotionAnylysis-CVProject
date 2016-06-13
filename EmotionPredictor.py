from skimage.feature import hog
import numpy as np
import cv2
from sklearn import svm
import time

class EmotionPredictor:
    def computeSimilarityToStandardEmotion(self,scores,standard):
        size=len(standard[0])
        stretchedScores=[]
        for i in range(8):
            temp=[0]*size
            stretchedScores.append(temp)
        
        for i in range(size):
            j=int(i*len(scores[0])/len(stretchedScores[0]))
            #print str(i)+" "+str(j)
            for x in range(8):
                stretchedScores[x][i]=scores[x][j]
                
        difference=0
        for i in range(size):
            for j in range(8):
                difference+=abs(standard[j][i]-stretchedScores[j][i])
                #print abs(standard[j][i]-stretchedScores[j][i])
        
        maxDifference=0
        for i in range(size):
            for j in range(8):
                if standard[j][i]<0.5:
                    maxDifference+=(1-standard[j][i])
                else:
                    maxDifference+=standard[j][i]
        
        similarity=(maxDifference-difference)/maxDifference*100
        
        #print difference,maxDifference
        return similarity,stretchedScores
        
    
    def adjustEmotionScores(self,probaResult,metric):
    	pool=0
    	for i in range(8):
    		if metric[i]<0:
    			pool+=probaResult[0,i]*abs(metric[i])
    			probaResult[0,i]*=1+metric[i]
    	for i in range(8):
    		if metric[i]>0:
    			probaResult[0,i]+=pool*metric[i]

    	#print pool
    	return probaResult
    
    def startPredictionFromCamera(self,clf,featureMeans,featureVariance,metric,timeLimit):
        #test
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml') 
        cap = cv2.VideoCapture(0)

        #####time domain
        smoothBuffer=[[],[],[],[],[],[],[],[]]
        plotBuffer=[[0.125],[0.125],[0.125],[0.125],[0.125],[0.125],[0.125],[0.125]]
        timeInterval=0.5
        lastUpdatedTime=time.time()
        startTime=time.time()
        #####
        probaResult=np.array([[0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125]])
        textLabelMap={0.0:'Neutral',1.0:'Anger',2.0:'Contempt',3.0:'Disgust',4.0:'Fear',5.0:'Happy',6.0:'Sadness',7.0:'Surprise'}
        while(time.time()-startTime<timeLimit):
            # Capture frame-by-frame
            #print time.time()-startTime
            ret, frame = cap.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            textResult="No face"
    
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces)>1:
                textResult="Error: Multi Faces"
                continue
    
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray,(256, 256), interpolation = cv2.INTER_CUBIC)
                
                            
                #testImageFeatures=[]
                #for i in range(4):
                #    for j in range(4):
                #        patch=roi_gray[i*64:(i+1)*64,j*64:(j+1)*64]
                #        fd, hog_image = hog(patch, orientations=8, pixels_per_cell=(16, 16),cells_per_block=(1, 1), visualise=True)
                #        testImageFeatures.extend(fd)
                testImageFeatures, hog_image = hog(roi_gray, orientations=8, pixels_per_cell=(32, 32),cells_per_block=(3, 3), visualise=True)
            
                testImageFeatures=np.array(testImageFeatures)
                testImageFeatures-=featureMeans
                testImageFeatures/=featureVariance
                probaResult=clf.predict_proba(np.array(testImageFeatures).reshape(1, -1))
                probaResult=self.adjustEmotionScores(probaResult,metric)


                maxIndex=0
                maxValue=0
                for r in range(8):
                	if probaResult[0,r]>maxValue:
                		maxValue=probaResult[0,r]
                		maxIndex=r
                textResult=textLabelMap[maxIndex]
                #print resultLabel
        
                #####show on screen
                
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                for index in range(8):
                    textTemp=textLabelMap[float(index)]
                    probTemp=probaResult[0,index]
                    cv2.putText(frame,textTemp, (40,40+index*40), cv2.FONT_HERSHEY_SIMPLEX, 1 ,[100,100,255],2)
                    cv2.rectangle(frame,(200,25+index*40),(200+int(100*probTemp),40+index*40),(100,100,255),2)
                #######
        
            #######time-domain
            if time.time()-lastUpdatedTime>timeInterval:
                #print "~~"
                for index in range(8):
                    #print "!!"
                    #print np.mean(smoothBuffer[index])
                    #print plotBuffer[index][-1]+np.mean(smoothBuffer[index])
                    if len(smoothBuffer[index])==0:
                        plotBuffer[index].append(plotBuffer[index][-1])
                    else:
                        plotBuffer[index].append((plotBuffer[index][-1]+np.mean(smoothBuffer[index]))/2)
                    smoothBuffer[index]=[]
                        
                    
                sumTemp=0   #normalization
                for index in range(8):
                    sumTemp+=plotBuffer[index][-1]
                    
                if sumTemp!=0:
                    for index in range(8):
                        plotBuffer[index][-1]/=sumTemp
                  
                lastUpdatedTime=time.time()
            else:
                for index in range(8):
                    smoothBuffer[index].append(probaResult[0,index])
            #######

        
            cv2.putText(frame,textResult, (35,400), cv2.FONT_HERSHEY_SIMPLEX, 2, [100,100,255],5)
            cv2.putText(frame,"Press Q to quit", (800,50), cv2.FONT_HERSHEY_SIMPLEX, 1, [100,100,255],2)
            # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        return plotBuffer
    
    def predictOneImage(self,clf,frame,featureMeans,featureVariance,metric):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

        textLabelMap={0.0:'Neutral',1.0:'Anger',2.0:'Contempt',3.0:'Disgust',4.0:'Fear',5.0:'Happy',6.0:'Sadness',7.0:'Surprise'}
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        textResult="No face"
    
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #print(len(faces))
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray,(256, 256), interpolation = cv2.INTER_CUBIC)
                                    
            #testImageFeatures=[]
            #for i in range(4):
            #    for j in range(4):
            #        patch=roi_gray[i*64:(i+1)*64,j*64:(j+1)*64]
            #        testfd, hog_image = hog(patch, orientations=8, pixels_per_cell=(16, 16),cells_per_block=(1, 1), visualise=True)
            #        testImageFeatures.extend(testfd)
            testImageFeatures, hog_image = hog(roi_gray, orientations=8, pixels_per_cell=(32, 32),cells_per_block=(3, 3), visualise=True)

            
            testImageFeatures=np.array(testImageFeatures)
            testImageFeatures-=featureMeans
            testImageFeatures/=featureVariance

            probaResult=clf.predict_proba(np.array(testImageFeatures).reshape(1, -1))
            probaResult=self.adjustEmotionScores(probaResult,metric)

            maxIndex=0
            maxValue=0
            for r in range(8):
            	if probaResult[0,r]>maxValue:
            		maxValue=probaResult[0,r]
               		maxIndex=r
            textResult=textLabelMap[maxIndex]
            #print testImageFeatures
            #print resultLabel
    
            #####show on screen
            #print probaResult
            for index in range(8):
                textTemp=textLabelMap[float(index)]
                probTemp=probaResult[0,index]
                cv2.putText(frame,textTemp, (40,40+index*40), cv2.FONT_HERSHEY_SIMPLEX, 1 ,[100,100,255],2)
                cv2.rectangle(frame,(200,25+index*40),(200+int(100*probTemp),40+index*40),(100,100,255),2)
                #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            #######
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    
        cv2.putText(frame,textResult, (35,400), cv2.FONT_HERSHEY_SIMPLEX, 2, [100,100,255],5)
            # Display the resulting frame
        cv2.imshow('frame',frame)
        cv2.waitKey()
        cv2.destroyAllWindows()