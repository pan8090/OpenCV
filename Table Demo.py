import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x=np.random.rand(5,8)*.7
plt.plot(x.mean(axis=0),'-o',label='average per column')
plt.xticks([])
plt.table(cellText=[['%1.2f' % xxx for xxx in xx] for xx in x],cellColours=plt.cm.GnBu(x),loc='bottom')
plt.show()