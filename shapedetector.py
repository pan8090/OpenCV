'''
定义形状检测器
编写代码封装形状识别逻辑
'''

import cv2.cv2 as cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self,c):
        #初始化形状名称并近似轮廓
        shape=" unidentified"
        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.04*peri,True)
        #如果3个顶点，则是三角形
        if len(approx) == 3:
            shape=" triangle "
            #如果形状有四个顶点，则可以是正方形或矩形
        elif len(approx)==4:
            #计算轮廓的边界框并使用边界框计算纵横比
            (x,y,w,h)=cv2.boundingRect(approx)
            ar=w/float(h)
            #正方形的纵横比大约为1，否则为矩形
            shape=" square " if ar>=0.95 and ar<=1.05 else " rectangle "
            #如果5个顶点，则是五边形
        elif len(approx)==5:
            shape=" pentagon "
            #否则，假设形状为圆形
        else:
            shape=" circle "
            #返回形状的名称
        return shape