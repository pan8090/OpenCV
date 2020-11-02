import cv2
import imutils

image=cv2.imread("imgs/zlj.jpg")
(h,w,d)=image.shape
print("width={},height={},depth={}".format(w,h,d))

roi=image[60:260,320:520]
cv2.imshow("ROI",roi)

cv2.imshow("image",image)
cv2.waitKey(0)

r=300.0/w
dim=(300,int(h*r))
resized=cv2.resize(image,dim)
cv2.imshow("Aspect Ratio Resize",resized)
cv2.waitKey(0)

#高斯模糊方法
blurred=cv2.GaussianBlur(image,(11,11),0)
cv2.imshow("Blurred",blurred)
cv2.waitKey(0)


#图像上绘图
output=image.copy()
cv2.rectangle(output,(300,60),(410,185),(0,0,255),2)
cv2.imshow("Rectangle",output)
cv2.waitKey(0)

output = image.copy()
cv2.circle(output, (300, 150), 20, (255, 0, 0), -1)
cv2.imshow("Circle", output)
cv2.waitKey(0)

output = image.copy()
cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)
cv2.imshow("Line", output)
cv2.waitKey(0)

output = image.copy()
cv2.putText(output, "OpenCV + Jurassic Park!!!", (10, 25),
	cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imshow("Text", output)
cv2.waitKey(0)
