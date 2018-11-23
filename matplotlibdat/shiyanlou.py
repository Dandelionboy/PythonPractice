import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_table('a.txt',encoding="utf8",sep=',',header=0)#sep=','取出，
#把时间转换成DatetimeIndex
times=pd.to_datetime(df["创建时间"])
#把原始数据进行时间序列化
df.index=times
#删除重复的创建时间
newdf=df.drop("创建时间",axis=1)
#安周采样
df_week=newdf.resample("W").sum()
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(df_week.index,df_week["学习时间"],'g--')
ax.set_xlabel("time")
ax.set_ylabel("study")
plt.show()