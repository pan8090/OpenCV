import numpy as np
# a0=np.array([1,2,3,4])
# a1=np.array((1,2,3,4))
# print(a0)
# print(a1)
#
# a2=np.array([[1,2,3],[2,3,4],[4,5,6]])
# print(a2)
#
# a3=np.arange(0,1,0.2)
# print(a3)
#
# a4=np.linspace(0,10,10)
# print(a4)
#
# a5=np.random.rand(2,2)
# a6=np.random.randn(2,2)
# a7=np.random.randint(0,9,(2,2))
# print(a5)
# print(a6)
# print(a7)
#
# a8=np.zeros(9)
# print(a8)
#
# print(a7.ndim)
# #二维数组
# b=np.arange(25).reshape(5,5)
# print(b)
# print(b[1,2:4])
#
# #三维数组
# b1=np.ones(45).reshape(3,5,3)
# b1[0,0,0]=8
# print(b1)
#
# b2=np.arange(0,10,1)
# b3=b2.reshape(2,5)
# print(b2)
# print(b3)
#
# b4=np.arange(0,10,1)
# b5=b4.reshape(2,-1)
# b6=b4.reshape(-1,5)
# print(b4)
# print(b5)
# print(b6)
#
# #数组的维度交换
# b7=np.arange(10).reshape(2,5)
# b8=b7.swapaxes(0,1)
# print(b7)
# print(b8)
#
# c=np.arange(24).reshape(2,3,4)
# d=c.swapaxes(0,1)
# print(c)
# print(d)

# #数组降维
# a=np.arange(10).reshape(2,5)
# c=a.reshape(-1)
# d=a.ravel()
# print(a)
# print(c)
# print(d)

#堆叠数组
a=np.array([1,2,3,4])
b=np.array([5,6,7,8])
c=np.hstack((a,b))
d=np.vstack((a,b))
print(c)
print(d)