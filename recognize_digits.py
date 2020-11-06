'''
使用OpenCV和Python识别数字
利用计算机视觉来识别恒温器上的数字
'''

from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2.cv2 as cv2

#定义数字段的字典，以便我们可以识别温控器上的每个数字
DIGITS_LOOKUP={
    (1,1,1,0,1,1,1):0,
    (0,0,1,0,0,1,0):1,
    (1,0,1,1,1,1,0):2,
    (1,0,1,1,0,1,1):3,
    (0,1,1,1,0,1,0):4,
    (1,1,0,1,0,1,1):5,
    (1,1,0,1,1,1,1):6,
    (1,0,1,0,0,1,0):7,
    (1,1,1,1,1,1,1):8,
    (1,1,1,1,0,1,1):9
}

#加载实例图片
image=cv2.imread("imgs/example.jpg")
#通过调整图像大小来预处理图像，将其转换为灰度，对其进行模糊处理，然后计算边缘图
image=imutils.resize(image,height=500)  #调整大小
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #图像转换为灰度
blurred=cv2.GaussianBlur(gray,(5,5),0)  #对5*5内核应用高斯模糊，以减少高频噪声
edged=cv2.Canny(blurred,50,200,255)  #通过Canny边缘检测器计算边缘图

#提取LCD本身
#在边缘贴图中找到轮廓，然后按其轮廓大小降序排序
cnts=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,
                 cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)
cnts=sorted(cnts,key=cv2.contourArea,reverse=True)
displayCnt=None
#在轮廓上循环
for c in cnts:
    #近似轮廓
    peri=cv2.arcLength(c,True)
    approx=cv2.approxPolyDP(c,0.02*peri,True)

    if len(approx)==4:
        displayCnt=approx
        break

#获得四个顶点后，我们可以通过四点透视变换提取LCD：
warped=four_point_transform(gray,displayCnt.reshape(4,2))
output=four_point_transform(image,displayCnt.reshape(4,2))

#从LCD提取数字：
#设定变形图像的阈值，然后应用一系列形态操作以清理阈值图像
thresh=cv2.threshold(warped,0,255,
                     cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) [1]
kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,5))
thresh=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)

#应用轮廓滤波，寻找实际的数字
#在阈值图像中找到轮廓，初始化轮廓列表
cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,
                      cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)
digitCnts=[]
#遍历数字区域候选者
for c in cnts:
#计算轮廓的边界框
    (x,y,w,h)=cv2.boundingRect(c)
#如果轮廓足够大，则必须为数字
    if w>=15 and (h>=30 and h<=40):
        digitCnts.append(c)

#识别每个数字
#从左到右对数字轮廓进行排序
digitCnts=contours.sort_contours(digitCnts,
                                 method="left-to-right")[0]
digits=[]

#实际识别过程：
for c in digitCnts:  #遍历每个数字轮廓
    #计算区域中的边界框并提取数字ROI
    (x,y,w,h)=cv2.boundingRect(c)
    roi=thresh[y:y+h,x:x+w]
    #根据ROI尺寸计算出每个分段的大致宽度和高度
    (roiH,roiW)=roi.shape
    (dW,dH)=(int(roiW*0.25),int(roiH*0.15))
    dHC=int(roiH*0.05)

    segments=[
        ((0, 0), (w, dH)),  # top
        ((0, 0), (dW, h // 2)),  # top-left
        ((w - dW, 0), (w, h // 2)),  # top-right
        ((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # center
        ((0, h // 2), (dW, h)),  # bottom-left
        ((w - dW, h // 2), (w, h)),  # bottom-right
        ((0, h - dH), (w, h))  # bottom
    ]
    on=[0]*len(segments)

    #在段上循环，遍历每个线段的（x,y）坐标
    for (i,((xA,yA),(xB,yB))) in enumerate(segments):
        #提取段ROI
        segROI=roi[yA:yB,xA:xB]
        total=cv2.countNonZero(segROI)
        area=(xB-xA)*(yB-yA)

        if total / float(area) >0.5:
            on[i]=1

    digit=DIGITS_LOOKUP[tuple(on)]
    digits.append(digit)
    cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),1)
    cv2.putText(output,str(digit),(x-10,y-10),
                cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,255,0),2)

#将数字打印到屏幕并显示图像
print(u"{}{}.{} \u00b0c".format(*digits))
cv2.imshow("Input",image)
cv2.imshow("Output",output)
cv2.waitKey(0)