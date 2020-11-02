import numpy as np
import operator

def createDataSet():
    '''
    构建假的训练数据，产生四条训练样本，group为样本属性，labels为分类标签，即【1.0，1.1】属于A类
    :return:
    '''
    group=np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels

def classify(inX,dataSet,labels,k):
    '''
    简单KNN分类
    :param inX:待分类向量
    :param dataSet: 训练样本集
    :param labels: 训练样本标签
    :param k: K值
    :return:
    '''
    dataSetSize=dataSet.shape[0]    #训练样本个数
    diffMat=np.tile(inX,(dataSetSize,1))-dataSet  #计算训练样本和待分类样本的数值差值
    # 用于后面计算欧式距离，欧式距离为各维度上数值差值的平方和再开方的结果
    sqDiffMat=diffMat**2            #差值的平方
    sqDistances=sqDiffMat.sum(axis=1)  #平方和
    distances=sqDistances**0.5         #平方和开方
    sortedDistIndicies=distances.argsort()  #返回升序排列后的序列
    classCount={}
    #统计前K个样本中各标签出现次数
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    #按标签次数排序，返回次数最多的标签
    return sortedClassCount[0][0]

if __name__=='__main__':
    group,labels=createDataSet()
    print(classify([0,0],group,labels,2))
    #最终输出类别为B

    #print(classify([1.0, 0], group, labels, 2))
    #最终输出类别为A