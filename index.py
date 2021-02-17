import cv2
import numpy as np
import utils

path = "./image/3.jpeg"

img = cv2.imread(path)

imgBlank = np.zeros((480,640,3),np.uint8)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(img,(5,5),1)

# imgCanny = cv2.Canny(imgBlur,90,140)
imgCanny = cv2.Canny(imgBlur,65,55)
kernel = np.ones((5,5))
imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
imgErode = cv2.erode(imgDial,kernel,iterations=1)

# FINDING THE CONTOURS
imgContours = img.copy()
imgBigContours = img.copy()

ctn, c = cv2.findContours(imgErode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
max_area = 0
for c in ctn:
	area = cv2.contourArea(c)
	# print(area)
	if area > 5000:
		cv2.drawContours(imgContours,c, -1, (0,255,0),5)
		peri = cv2.arcLength(c,True)
		approx = cv2.approxPolyDP(c,0.02*peri,True)
		if area> max_area and (len(approx)) == 4:
			biggest = approx
			max_area = area
			# biggest = utils.reorder(biggest)
			cv2.drawContours(imgBigContours, c, -1,(0,0,255),5)
			cv2.drawContours(imgBigContours, biggest, -1,(0,255,0),20)

			w_img = 437
			h_img = 236
			
			p1 = [0,0]
			p2 = [w_img,0]
			p3 = [0,h_img]
			p4 = [w_img,h_img]

			pts1 = np.float32(biggest)
			# pts2 = np.float32([p3,p1,p2,p4])
			pts2 = np.float32([p2,p4,p3,p1])
			matrix = cv2.getPerspectiveTransform(pts1, pts2)
			imgWarpColored = cv2.warpPerspective(img, matrix, (w_img,h_img))
			imgWarpColored = imgWarpColored[10:imgWarpColored.shape[0]-10,10:imgWarpColored.shape[1]-10]
			imgWarpColored = cv2.resize(imgWarpColored,(w_img,h_img))
			
			# applying adaptive threshold
			imgWarpGrap = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
			imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGrap, 255,1,1,7,2)
			imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
			# imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre,1)




# cv2.imshow("img", img)
# cv2.imshow("imgGray", imgGray)
# cv2.imshow("imgBlur", imgBlur)
# cv2.imshow("imgCanny", imgCanny)
# cv2.imshow("imgDial", imgDial)
# cv2.imshow("imgErode",imgErode)
# cv2.imshow("output", imgContours)
cv2.resize(imgWarpColored, (480, 680))
cv2.imshow("Scanning ...", imgBigContours)
cv2.imshow("scanned img", imgWarpColored)
cv2.imshow("scanned printed image", imgAdaptiveThre)
count = 0
cv2.imwrite('saved-images/'+str(count)+".jpg",imgWarpColored)
count += 1
	
cv2.waitKey(0)
	