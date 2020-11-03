import cv2
from imutils import paths
import numpy as np
import argparse
import  imutils

ap=argparse.ArgumentParser()
ap.add_argument("-i","--images",type=str,required=True,
                help="输出要拼接图像的目录的路径")
ap.add_argument("-o","--output",type=str,required=True,
                help="输出图像的路径")
args=vars(ap.parse_args())

#获取输入图像的路径并初始化我们的图像列表
print("[INFO] loading images...")
imagePaths=sorted(list(paths.list_images(args["images"])))
images=[]
#遍历图像路径，加载每个图像路径，然后将其添加到列表图像
for imagePath in imagePaths:
    image=cv2.imread(imagePath)
    images.append(image)
#初始化OpenCV的图像拼接器对象，然后执行图像拼接
print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)
# 如果状态为0，则OpenCV成功执行了图像拼接
if status == 0:
	# 将输出的拼接图像写入磁盘
	cv2.imwrite(args["output"], stitched)
	# 在屏幕上显示输出的拼接图像
	cv2.imshow("Stitched", stitched)
	cv2.waitKey(0)
# 否则拼接失败，可能是由于被检测到的关键点不足造成的
else:
	print("[INFO] image stitching failed ({})".format(status))

	#启动命令：
	#python image_stitching_simple.py --images imgs/scottsdale --output output.png

