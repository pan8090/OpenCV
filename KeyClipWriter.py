from collections import deque
from threading import Thread
from queue import  Queue
import time
import cv2

class KeyClipWriter:
    def __init__(self,bufSize=64,timeout=1.0):
        #要保留在内存缓冲区中的最大帧数
        self.bufSize=bufSize
        self.timeout=timeout

        #用于存储最大数量的缓冲区bufsize从视频流中读取的帧
        self.frames=deque(maxlen=bufSize)
        #用于保存等待写入视频文件的帧
        self.Q=None
        #用于将帧实际写入输出视频文件的类
        self.writer=None
        #将视频写入文件时将使用的实例
        self.thread=None
        #指示我们是否处于“记录模式”
        self.recording=False

    def update(self, frame):
        # 更新帧缓冲区
        self.frames.appendleft(frame)
        # 如果我们正在录制，请同时更新队列
        if self.recording:
            self.Q.put(frame)

    #start方法创建了一个新线程，调用write在内部写入框架的方法归档到Q
    def start(self, outputPath, fourcc, fps):
        '''
        表示我们正在录制，启动视频编写器，
        初始化我们需要写入的帧队列到视频文件
        '''
        self.recording = True
        self.writer = cv2.VideoWriter(outputPath, fourcc, fps,
                                      (self.frames[0].shape[1], self.frames[0].shape[0]), True)
        self.Q = Queue()
        # 遍历双端队列结构中的帧并添加它们进入队列
        for i in range(len(self.frames), 0, -1):
            self.Q.put(self.frames[i - 1])
        # 启动线程将帧写入视频文件
        self.thread = Thread(target=self.write, args=())
        self.thread.daemon = True
        self.thread.start()

    def write(self):
        # 继续循环
        while True:
            # 如果完成录制，退出线程
            if not self.recording:
                return
            # 检查队列中是否有条目
            if not self.Q.empty():
                # 抓取队列中的下一帧并将其写入到视频文件
                frame = self.Q.get()
                self.writer.write(frame)
            # 否则，队列为空，sleep一会，这样就不会浪费CPU周期
            else:
                time.sleep(self.timeout)

    def flush(self):
        #通过将所有剩余帧刷新到文件来清空队列
        while not self.Q.empty():
            frame=self.Q.get()
            self.writer.write(frame)

    def finish(self):
        #表示我们已经完成记录，加入线程，将队列中所有剩余的帧刷新到文件
        #然后释放writer指针
        self.recording=False
        self.thread.join()
        self.flush()
        self.writer.release()