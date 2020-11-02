import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#定义序列长度
L = 2**10
#定义方差列表
sigma_list = [3, 2, 1]
#生成三个高斯随机序列,并保留一位小数
gs_1 = np.round(np.random.randn(L, 1) * sigma_list[0], 1)
gs_2 = np.round(np.random.randn(L, 1) * sigma_list[1], 1)
gs_3 = np.round(np.random.randn(L, 1) * sigma_list[2], 1)

#统计校验方差
#使用np.std
print("序列1方差理论值 = {}，统计估计值 = {}".format(sigma_list[0], np.std(gs_1, ddof = 1)))
print("序列2方差理论值 = {}，统计估计值 = {}".format(sigma_list[1], np.std(gs_2, ddof = 1)))
print("序列3方差理论值 = {}，统计估计值 = {}".format(sigma_list[2], np.std(gs_3, ddof = 1)))

ga = np.hstack((gs_1, gs_2, gs_3))
print("连接后矩阵的维度 = {}".format(ga.shape))

#gdf = pd.DataFrame(ga, columns = [str(sigma_list[0]), str(sigma_list[1]), str(sigma_list[2])])
gdf = pd.DataFrame(ga, columns = ['A', 'B', 'C'])
#打印前10个
print(gdf[0:10])

plt.plot(gdf)
plt.xlabel("index")
plt.ylabel("value")
plt.title("before")
plt.legend(("sigma = "+str(sigma_list[0]),"sigma = "+str(sigma_list[1]),"sigma = "+str(sigma_list[2])))
plt.show()
