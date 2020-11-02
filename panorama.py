#导入必要的包
import numpy as np
import imutils
import cv2

class Stitcher:
    def __init__(self):
        #确定我们在使用OpenCV v3.x
        self.isv3=imutils.is_cv3(or_better=True)

    def stitch(self, images, ratio=0.75, reprojThresh=4.0,
               showMatches=False):
        # 解压缩图像，然后检测关键点并提取来自它们的局部不变描述符
        (imageB, imageA) = images
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)
        # 匹配两个图像之间的特征
        M = self.matchKeypoints(kpsA, kpsB,
                                featuresA, featuresB, ratio, reprojThresh)
        # 如果匹配为”无“，则创建全景的关键点不足
        if M is None:
            return None

        # 否则，应用透视变换缝合图像
        (matches,H,status)=M
        result = cv2.warpPerspective(imageA, H,
                                     (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
        # 检查关键点匹配是否应该可视化
        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches,
                                   status)
            # 返回拼接图像的元组和可视化结果
            return (result, vis)
        # 返回拼接图像
        return result

    def detectAndDescribe(self, image):
        # 将图像转换为灰度
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # check to see if we are using OpenCV 3.X
        if self.isv3:
            # 检测并提取图像中的特征
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(image, None)
        # otherwise, we are using OpenCV 2.4.X
        else:
            # detect keypoints in the image
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)
            # 从图像中提取特征
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)
        # 将关键点KeyPoint对象转换为Numpy数组
        kps = np.float32([kp.pt for kp in kps])
        # 返回关键点和功能的元组
        return (kps, features)

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
                       ratio, reprojThresh):
        # 计算原始匹配并初始化实际列表
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
        # 循环原始匹配
        for m in rawMatches:
            # 确保距离在一定的比例之内
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        # 计算单应性至少需要4个匹配项
        if len(matches) > 4:
			#构造两组点
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])
            # 计算两组点之间的单应性
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
				reprojThresh)
            # 返回匹配项以及纯矩阵和每个匹配点的状态
            return (matches, H, status)
        # 否则，无法计算单应性
        return None

    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # 初始化输出可视化图像
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB
        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # 仅在关键点成功后处理匹配
            if s == 1:
                # draw the match
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
        # return the visualization
        return vis