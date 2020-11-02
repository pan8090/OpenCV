import cv2

# 读取文件
image = 'imgs/555.jpg'
model = 'venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml'
# 读取图片
image = cv2.imread(image)
# 加载模型
model = cv2.CascadeClassifier(model)

# 人脸检测
faces = model.detectMultiScale(image)
for (x, y, w, h) in faces:
    # 画出人脸矩形框
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

# 显示和保存图片
cv2.imshow('result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('imgs/result.jpg', image)
print('已保存')



# import cv2
#
# #读取图片
# image=cv2.imread('imgs/111.jpg')
#
# #加载人脸模型库
# face_model=cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
#
# #图片进行灰度处理
# grap=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#
# #人脸检测
# faces=face_model.detectMultiScale(grap)
#
# #标记人脸
# for(x,y,w,h) in faces:
#     cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
#
# #显示图片窗口
# cv2.imshow('faces',image)
#
# #窗口暂停
# cv2.waitKey(0)
#
# #销毁窗口资源
# cv2.destroyWindow()