# import the necessary packages
import numpy as np
import cv2
def order_points(pts):
	'''
初始化将要订购的坐标列表因此列表中的第一个条目位于左上角，第二个条目是右上角，第三个条目是右下角，第四个是左下角
	'''
	rect = np.zeros((4, 2), dtype = "float32")
	# 左上点的总和最小，而右下点的总和最大
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	'''现在，计算点之间的差，右上角的差异最小，而左下角的差异最大'''
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	#返回有序坐标
	return rect
def four_point_transform(image, pts):
	#获得一致的点顺序并分别解压
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	'''计算新图像的宽度，该宽度将是右下角和左下角x坐标或右上角和左上角x坐标之间的最大距离'''
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	'''计算新图像的高度，该高度将是右上角和右下角y坐标或左上角和左下角y坐标之间的最大距离'''
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	'''现在我们有了新图像的尺寸，构造目标点集以获得图像的“鸟瞰图”（即俯视图），再次在左上角，右上角指定点 ，右下和左下顺序'''
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# 计算透视变换矩阵，然后应用它
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# 返回变形的图像
	return warped