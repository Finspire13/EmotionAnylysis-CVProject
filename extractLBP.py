# import the necessary packages
from skimage import feature
import numpy as np
import cv2
 
class LocalBinaryPatterns:
	def __init__(self, numPoints, radius):
		# store the number of points and radius
		self.numPoints = numPoints
		self.radius = radius
 
	def describe(self, image, eps=1e-7):
		# compute the Local Binary Pattern representation
		# of the image, and then use the LBP representation
		# to build the histogram of patterns

		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
		eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml') 
		faces = face_cascade.detectMultiScale(image, 1.3, 5)
		eye_x=[1]*2;
		eye_y=[1]*2;
		r_angle=0;
		for (x,y,w,h) in faces:
			roi_gray = image[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			i=0;
			for (ex,ey,ew,eh) in eyes:
				eye_x[i]=ex;
				eye_y[i]=ey;
				i=i+1;
		num_rows, num_cols = image.shape[:2]
		if np.absolute(eye_y[1]-eye_y[0])>3:
			a= np.array([eye_x[1]-eye_x[0],eye_y[1]-eye_y[0]])
			b = np.array([1, 0])
			la=np.sqrt(a.dot(a))
			lb=np.sqrt(b.dot(b))
			cos_angle=a.dot(b)/(la*lb)
			angle=np.arccos(cos_angle)
			print eye_y[1],eye_y[0]
			print  eye_y[1]-eye_y[0]
			angle2=angle*360/2/np.pi
			if eye_x[1]<eye_x[0]:
				r_angle=-(min(180-angle2,angle2))
			else:
				r_angle=min(180-angle2,angle2)
				print r_angle
		rotation_matrix = cv2.getRotationMatrix2D((x+w/2, y+h/2), r_angle, 1)
		img = cv2.warpAffine(image, rotation_matrix, (num_cols, num_rows))

		faces = face_cascade.detectMultiScale(img, 1.3, 5)
		for (rx,ry,rw,rh) in faces:
			cv2.rectangle(img,(rx,ry),(rx+rw,ry+rh),(255,0,0),2)
			print rx,ry,rw,rh
			img = img[ry:ry+rh, rx:rx+rw]
		res=cv2.resize(img,(256,256),interpolation=cv2.INTER_CUBIC)
		combinehist=[]
		weight=[[0]*8,[0,1,1,1,1,1,1,0],[1,4,4,4,4,4,4,1],[1,4,4,4,4,4,4,1],[0,1,1,1,1,1,1,0],[0,2,2,2,2,2,2,0],[0,2,4,4,4,4,2,0],[0,1,2,4,4,2,1,0]]
		for r in range (8):
			for c in range (8):
				crop_img = res[c*32+1:(c+1)*32, r*32+1:(r+1)*32]
				lbp = feature.local_binary_pattern(crop_img, self.numPoints, self.radius, method="uniform")
				(hist, _) = np.histogram(lbp.ravel(),
				bins=np.arange(0, self.numPoints + 3),
				range=(0, self.numPoints + 2))
				 # normalize the histogram
				hist = hist.astype("float")
				hist /= (hist.sum() + eps)
				hist = hist*weight[r][c]
				combinehist.extend( hist )
				# return the histogram of Local Binary Patterns
		return combinehist
	
