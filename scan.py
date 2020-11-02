#一个简单的文件扫描仪

from transform import four_point_transform
from skimage.filters import threshold_local
import argparse
import cv2
import imutils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

#加载图像并计算旧高度的比例
#达到新的高度，克隆它，并调整其大小
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
# 将图像转换为灰度，使其模糊并找到边缘
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
# 显示原始图像和边缘检测图像
print("STEP 1: 应用边缘检测")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

#寻找轮廓
# 在边缘图像中找到轮廓，仅保留
# 个最大的，并初始化屏幕轮廓
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
# 在轮廓上循环
for c in cnts:
	# 近似轮廓
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
     #如果我们的近似轮廓有四个点，那么我们
     #可以假设我们已经找到我们的屏幕
	if len(approx) == 4:
		screenCnt = approx
		break
# 显示纸的轮廓（轮廓）
print("STEP 2: 扫描文件轮廓")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


#应用四点变换以获得自顶向下
#查看原始图像
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
#将变形的图像转换为灰度，然后对其进行阈值处理
#赋予其“黑白”纸效果
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255
# 显示原始图像和扫描图像
print("STEP 3: 应用透视变换和阈值")
cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)
#python scan.py -i imgs/receipt.jpg

