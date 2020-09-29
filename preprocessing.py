# coding=utf8
import pandas as pd
import numpy as np


tagMap = {}
df = pd.read_csv('./data/topic2tags.csv')
print(df.columns)


df = df[['category','topic','tags']]
print(df.head())

df.to_csv("./data/topic2tags.csv",sep="\t",index=False,header=False)



df = pd.read_csv('./data/invalidTags.csv')
print(df.columns)


df = df[['tag']]
print(df.head())

df.to_csv("./data/invalidTags.csv",sep="\t",index=False,header=False)

