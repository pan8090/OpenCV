import cv2
import time
import numpy as np

# 读取图片
image = 'imgs/111.jpg'
image = cv2.imread(image)

# 级联分类器
model = cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')  # 加载模型
beg = time.time()
faces = model.detectMultiScale(image)
end = time.time()
print('级联分类器 {:.2f} s'.format(end - beg))

# DNN Caffe模型
net = cv2.dnn.readNetFromCaffe('dnn/deploy.prototxt', 'dnn/res10_300x300_ssd_iter_140000_fp16.caffemodel')  # Caffe模型
beg = time.time()
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
net.setInput(blob)
detections = net.forward()
end = time.time()
print('DNN Caffe模型 {:.2f} s'.format(end - beg))

# DNN TensorFlow模型
net = cv2.dnn.readNetFromTensorflow('dnn/opencv_face_detector_uint8.pb', 'dnn/opencv_face_detector.pbtxt')  # TensorFlow模型
beg = time.time()
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
net.setInput(blob)
detections = net.forward()
end = time.time()
print('DNN TensorFlow模型 {:.2f} s'.format(end - beg))