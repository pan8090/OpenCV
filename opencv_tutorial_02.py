#计数对象
# 导入必要的软件包，包括python自带的命令行参数解析包argparse
import argparse
import imutils
import cv2

#构造参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image")
args = vars(ap.parse_args())

#1、将彩色图像转换为灰度图像
# 加载图像（路径包含在命令行参数中）并且显示
image = cv2.imread(args["image"])
print("STEP 1：加载图像")
cv2.imshow("Image", image)
cv2.waitKey(0)
# 转换图像为灰度图像，需要image和cv2.COLOR_BGR2GRAY标志
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("STEP 1: 转换图像为灰度图像")
cv2.imshow("Gray", gray)
cv2.waitKey(0)

# 2、边缘检测
#应用边缘检测找到图像中目标物体的轮廓
edged = cv2.Canny(gray, 30, 150)
print("STEP 2: 边缘检测")
cv2.imshow("Edged", edged)
cv2.waitKey(0)

#3.灰度图像求阈值
# 所有灰度值<225的像素点设置为255（白色）-俄罗斯方块
# 灰度值>=225且<=255的像素点设置为0（黑色）——背景
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
print("STEP 3: 灰度图像求阈值")
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

#4.检测、计数和绘制轮廓
# 在图像中找到前景物体的轮廓
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()
# 循环绘制轮廓
for c in cnts:
    # 以紫色线条绘制轮廓
    # 一次显示一个物体的轮廓
    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
    print("STEP 4: 绘制轮廓")
    cv2.imshow("Contours", output)
    cv2.waitKey(0)
# 注明紫色轮廓的个数
text = "I found {} objects!".format(len(cnts))
cv2.putText(output, text, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
    (240, 0, 159), 2)
print("STEP 4: 标注轮廓数目")
cv2.imshow("Contours", output)
cv2.waitKey(0)

#5、腐蚀和膨胀
#通过腐蚀减小前景物体的尺寸，利用cv2.erode将轮廓尺寸减小5
mask = thresh.copy()
mask = cv2.erode(mask, None, iterations=5)
print("STEP 5: 腐蚀")
cv2.imshow("Eroded", mask)
cv2.waitKey(0)

# 膨胀可以扩大前景对象的尺寸
mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations=5)
print("STEP 5: 膨胀")
cv2.imshow("Dilated", mask)
cv2.waitKey(0)

#6、遮罩图像
#我们可能要应用的典型操作是遮盖图像某部分
#对输入图像按位与
# regions
mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask=mask)
print("STEP 6: 遮罩图像")
cv2.imshow("Output", output)
cv2.waitKey(0)

#7、运行脚本
#>python opencv_tutorial_02.py --image imgs/tx.jpg
