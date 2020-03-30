import cv2
import numpy as np
file_name = "inputImages/louder.jpeg"

src = cv2.imread(file_name, 1)
tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
lower = 50
band = 100
edgesim = cv2.Canny(tmp, lower, lower+band)
srcedges = cv2.cvtColor(edgesim, cv2.COLOR_GRAY2BGR)
_,alpha = cv2.threshold(edgesim, 0, 255, cv2.THRESH_BINARY)
b, g, r = cv2.split(srcedges)
rgba = [b,g,r, alpha]
dst = cv2.merge(rgba,4)
thickness = 1
dilated = cv2.dilate(dst, np.ones((thickness, thickness)))
cv2.imshow("main", dilated)
cv2.waitKey(2000)
cv2.imwrite("logo.png", dilated)