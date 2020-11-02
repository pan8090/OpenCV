import KeyClipWriter
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

#构造参数解析并解析参数
ap=argparse.ArgumentParser()
ap.add_argument("-o","--output",required=True,
                help="path to output directory") #输出目录的路径
ap.add_argument("-p","-picamera",type=int,default=-1,#是否应该使用Raspberry Pi相机
                help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f","-fps",type=int,default=20,
                help="FPS of output video")#输出视频的FPS
ap.add_argument("-c","--codec",type=str,default="MJPG",
                help="codec of output video")#输出视频的编解码器
ap.add_argument("-b","--buffer-size",type=int,default=32,
                help="buffer size of video clip writer")#视频剪辑编写器的缓冲区大小
args=vars(ap.parse_args())

#初始化视频流，并允许摄像头传感器 “warmup”
print("[INFO] warming up camera...")
vs=VideoStream(usePiCamera=args["picamera"]>0).start()
time.sleep(2.0)

#定义“绿色"球的上下边界在HSV颜色空间
greenLower=(29,86,6)
greenUpper=(64,255,255)
#初始化密钥剪辑的编写者和连续的编号
kcw=KeyClipWriter(bufSize=args["buffer_size"])
consecFrames=0

#保持循环
while True:
    '''
    抓取当前帧，调整其大小，然后初始化布尔值，用于指示是否连续帧，计数器应更新
    '''
    frame=vs.read()
    frame=imutils.resize(frame,width=600)
    updateConsecFrames=True
    #模糊帧并将其转换为HSV颜色空间
    blurred=cv2.GaussianBlur(frame,(11,11),0)
    hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)
    #为颜色”绿色“构建遮罩，然后进行一系列的扩张和腐蚀以出去小的遮罩中剩下的斑点
    mask=cv2.inRange(hsv,greenLower,greenUpper)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
    #在遮罩中找到轮廓
    cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)

    # 仅在发现至少一个轮廓时继续
    if len(cnts) > 0:
        # 找到遮罩中最大的轮廓，然后使用它计算最小的包围圈
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        updateConsecFrames = radius <= 10
        # 仅在半径达到最小尺寸的时候继续
        if radius > 10:
            consecFrames = 0
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 0, 255), 2)
            # 如果我们尚未录制，请开始录制
            if not kcw.recording:
                timestamp = datetime.datetime.now()
                p = "{}/{}.avi".format(args["output"],
                                       timestamp.strftime("%Y%m%d-%H%M%S"))
                kcw.start(p, cv2.VideoWriter_fourcc(*args["codec"]),
                          args["fps"])
    #否则，此框架中未执行任何操作，因此增加包含的连续帧数无动作
    if updateConsecFrames:
        consecFrames += 1
        # 更新关键帧剪辑缓冲区
    kcw.update(frame)
    # 如果我们正在录制并且无动作的帧数连续达到阈值，停止录制剪辑
    if kcw.recording and consecFrames == args["buffer_size"]:
        kcw.finish()
    # 显示框架
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # 如果按了q键，则从循环中中断
    if key == ord("q"):
        break

    # 如果我们正在录制剪辑，请把它包起来
    if kcw.recording:
        kcw.finish()
    # 清理
    cv2.destroyAllWindows()
    vs.stop()