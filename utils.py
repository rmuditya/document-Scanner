import numpy as np

def reorder(myPoints):
	myPoints = myPoints.reshape((4,2))
	myPointsNew = np.zeros((4,1,2), dtype=np.int32)
	add = myPoints.sum(1)

	myPointsNew[0] = myPoints[np.argmin(add)] 
	myPointsNew[3] = myPoints[np.argmin(add)] 
	diff = np.diff(myPoints, axis=1)
	myPointsNew[1] = myPoints[np.argmin(diff)] 
	myPointsNew[2] = myPoints[np.argmin(diff)] 
	return myPointsNew

pts2 = np.float32([[0,0],[w_img,0],[0,h_img],[w_img,h_img]])