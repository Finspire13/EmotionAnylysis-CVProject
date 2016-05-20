from extractLBP import LocalBinaryPatterns
from sklearn import svm
import os
import cv2
 
# initialize the local binary patterns descriptor along with
# the data and label lists
desc = LocalBinaryPatterns(24, 8)
data = []
sortedLabels = []

labelFile=open('data/label.txt')
rawLabels={}
for line in labelFile:
    lineWithoutN=line.split('\n')[0];
    elements=lineWithoutN.split(' ');
    strTemp=elements[-1]
    imageName=strTemp[:2]+"."+strTemp[3:]
    rawLabels[imageName]=elements[1:-1]


# loop over the training images
for imagePath in os.listdir('data/jaffe'):
	# load the image, convert it to grayscale, and describe it
    if imagePath!=".DS_Store":
        image = cv2.imread('data/jaffe/'+imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = desc.describe(gray)
        # extract the label from the image path, then update the
        # label and data lists
        sortedLabels.append(rawLabels[imagePath[:6]])
        data.append(hist)

print len(sortedLabels)
print len(data)

hapLabels = [float(x[0]) for x in sortedLabels]
hapRegressor=svm.SVR()
hapRegressor.fit(data,hapLabels)

sadLabels = [float(x[1]) for x in sortedLabels]
sadRegressor=svm.SVR()
sadRegressor.fit(data,sadLabels)

surLabels = [float(x[2]) for x in sortedLabels]
surRegressor=svm.SVR()
surRegressor.fit(data,surLabels)

angLabels = [float(x[3]) for x in sortedLabels]
angRegressor=svm.SVR()
angRegressor.fit(data,angLabels)

disLabels = [float(x[4]) for x in sortedLabels]
disRegressor=svm.SVR()
disRegressor.fit(data,disLabels)

feaLabels = [float(x[5]) for x in sortedLabels]
feaRegressor=svm.SVR()
feaRegressor.fit(data,feaLabels)


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

cap = cv2.VideoCapture(0)

while(True):

    ret,frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #for (x,y,w,h) in faces:
    #    roi_gray = gray[y:y+h, x:x+w]
    #    testData=[]
    #    hist = desc.describe(roi_gray)
    #    testData.append(hist)
        
    #    hap=hapRegressor.predict(testData)
    #    sad=sadRegressor.predict(testData)
    #    sur=surRegressor.predict(testData)
    #    ang=angRegressor.predict(testData)
    #    dis=disRegressor.predict(testData)
    #    fea=feaRegressor.predict(testData)
        
        #hap=(hap-min(hap))*5/(max(hap)-min(hap)+0.01)
        #sad=(sad-min(sad))*5/(max(sad)-min(sad)+0.01)
        #sur=(sur-min(sur))*5/(max(sur)-min(sur)+0.01)
        #ang=(ang-min(ang))*5/(max(ang)-min(ang)+0.01)
        #dis=(dis-min(dis))*5/(max(dis)-min(dis)+0.01)
        #fea=(fea-min(fea))*5/(max(fea)-min(fea)+0.01)
    #    print "hap: "+str(hap)
    #    print "sad: "+str(sad)
    #    print "sur: "+str(sur)
    #    print "ang: "+str(ang)
    #    print "dis: "+str(dis)
    #    print "fea: "+str(fea)
        # Display the resulting frame
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()