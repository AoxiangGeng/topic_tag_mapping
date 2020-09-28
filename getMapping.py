# coding=utf8
import pandas as pd
import numpy as np


tagMap = {}
df = pd.read_csv('topic2tags.csv')
print(df.columns)


df = df[[u'category',u'topics',u'tags']]
print(df.head())

df.to_csv("topicMap.csv",sep="\t",index=False,header=False)

