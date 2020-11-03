'''
Title：使用OpenCV和Python进行图像拼接
Content；本教程基于以下事实：我们能够手动执行关键点检测，特征提取和关键点匹配，
从而使得我们能够使用所用的单应性矩阵将我们的两个输入图像扭曲成全景图
'''
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
ap.add_argument("-c", "--crop", type=int, default=0,
	help="是否裁剪出最大的矩形区域")
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
    if args["crop"]>0:
        #在拼接图像周围创建10像素边框
        print("[INFO] cropping...")
        stitched=cv2.copyMakeBorder(stitched,10,10,10,10,
                                    cv2.BORDER_CONSTANT,(0,0,0))
        #将拼接的图像转换为灰度并对其进行阈值处理，将所有大于0的像素设置为255（前景）
        #而其他所有参数保持为0（背景）
        gray=cv2.cvtColor(stitched,cv2.COLOR_BGR2GRAY)
        thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY)[1]
         # 在阈值图像中找到所有外部轮廓，然后找到最大的轮廓就是拼接图像
        cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)
        cnts=imutils.grab_contours(cnts)
        c=max(cnts,key=cv2.contourArea)
        #为掩码分配内存，该掩码将包含拼接图像区域的矩形边界框
        mask=np.zeros(thresh.shape,dtype="uint8")
        (x,y,w,h)=cv2.boundingRect(c)
        cv2.rectangle(mask,(x,y),(x+w,y+h),255,-1)

        minRect=mask.copy()  #会逐渐减少尺寸，直到可以放入全景内部为止
        sub=mask.copy()    #用于确定是否需要继续减小minRect

        while cv2.countNonZero(sub)>0:  #继续循环，直到不再有前景像素为止
            minRect=cv2.erode(minRect,None)  #进行腐蚀操作以减小minRect
            sub=cv2.subtract(minRect,thresh) #一旦不再有前景像素minRect，就跳出循环
        #在最小矩形遮罩中找到轮廓，然后提取边界框（x，y）的坐标
        cnts=cv2.findContours(minRect.copy(),cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)
        cnts=imutils.grab_contours(cnts)
        c=max(cnts,key=cv2.contourArea) #抓取最大轮廓
        (x,y,w,h)=cv2.boundingRect(c)  #计算最大轮廓的边界框
        #使用边界框坐标提取最终的拼接图像
        stitched=stitched[y:y+h,x:x+w]
    #将输出的拼接图像写入磁盘
    cv2.imwrite(args["output"],stitched)
    #在屏幕上显示输出的拼接图像
    cv2.imshow("Stitched",stitched)
    cv2.waitKey(0)
#否则，拼接失败。可能是由于被检测到的关键点不足造成的
else:
    print("[INFO] image stitching failed ({})".format(status))

    '''
    版本为：
    opencv_python-4.2.0.32
    opencv-contrib-python-4.2.0.32
    
    启动命令为：
    python image_stitching.py --images imgs/scottsdale --output output.png --crop 1
    '''