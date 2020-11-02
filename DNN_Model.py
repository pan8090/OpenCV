import cv2
import numpy as np

#读取文件
image='imgs/555.jpg'
net=cv2.dnn.readNetFromCaffe('dnn/deploy.prototxt','dnn/res10_300x300_ssd_iter_140000_fp16.caffemodel')

#读取图片
image=cv2.imread(image)
height,width,channel=image.shape   #高，宽，通道数

#人脸检测
#调整大小并降低光照的影响
blob=cv2.dnn.blobFromImage(cv2.resize(image,(300,300)),1.0,(300,300),(104.0,177.0,123.0))
net.setInput(blob)  #设置输入
detections=net.forward()  #检测结果
faces=detections[0,0]   #人脸结果
for face in faces:
    confidence=face[2]  #置信度
    if confidence>0.5: 
        
        #置信度阈值设为0.5
        box=face[3:7]* np.array([width,height,width,height])  #人脸矩阵框坐标
        pt1=int(box[0]),int(box[1])  #左上角坐标
        pt2=int(box[2]),int(box[3])  #右下角坐标
        cv2.rectangle(image,pt1,pt2,(0,255,0),thickness=2)  #画出人脸矩阵框

        text='{:.2f}%'.format(confidence*100)  #置信度文本
        startX,startY=pt1
        y=startY-10 if startY -10>10 else startY +10
        org=(startX,y)  #文本的左下角坐标
        #画出置信度
        cv2.putText(image,text,org,cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),thickness=2)

    #显示和保存图片
    cv2.imshow('result',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('imgs/result.jpg',image)
    print('已保存')