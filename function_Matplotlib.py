import matplotlib.pyplot as plt
import numpy as np

x=np.linspace(0,10,100)
y=np.sin(x)
z=np.cos(x**2)
#调出画布，并指定画布的宽度和高度
plt.figure(figsize=(8,4))

plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2)
plt.plot(x,z,"b--",label="$cos(x^2)$")
#设置x轴，y轴的显示范围
plt.xlabel("Time(S)")
plt.ylabel("V")
#设置标题
plt.title("python basis -- matplotlib")
#分别设置x，y轴的显示范围
plt.ylim(-1.2,1.2)
#显示图例
plt.legend(loc=1)
plt.show()

#画直方图
a=np.random.randn(10000)
#bins代表直方图的长条形数目，默认为10；edgecolor代表长条行边框的颜色；alpha代表透明度
plt.hist(a,bins=40,facecolor="blue",edgecolor="black",alpha=0.7)
plt.show()

#读取图像
img=plt.imread("imgs/111.jpg")
print(img.dtype)
print(img.shape)
plt.imshow(img)
plt.show()

