# coding=utf8
import os
import numpy as np
import time
from langconv import *
import re
import sys
from collections import defaultdict

### 1 ### load vectors
tagName = []
tagVec = []
count = 0
for i in range(0,50):
    with open ('./vectors/part-000%02d'%i, 'r') as f:
        print('./vectors/part-000%02d'%i)
        for line in f.readlines():
            tag = line.strip().split('\t')[0]
            vec = line.strip().split('\t')[2].split(',')
            vec = np.array(vec, dtype=np.float64)
            tagVec.append(vec)
            tagName.append(tag)
            count += 1
            if count % 5000 == 0:
                print(count, tag)
                print(vec)

print(len(tagName),len(tagVec))
indexs = [tagName, tagVec]

'''
with open ('vectors.txt','w') as g:
    for key,vec in result.items():
        g.write(str(key)+'\t'+str(vec)+'\n')
'''

### 2 ### load topic2tag map
categoryMap = defaultdict(list)
topicMap = {}
with open ('./data/topic2tags.csv','r') as f:
    for line in f.readlines():
        try:
            category, topic, tags = line.strip().split('\t')
            tags = tags.split(',')
            categoryMap[category].append(topic)
            topicMap[topic] = tags
            print(category, topic)
            print(tags)
        except Exception as e:
            continue

### 3 ### vectors innere product
def search_vectors(user_vec, count, index):
    #暴力计算返回内积结果最大的向量
    ids = index[0]
    vectors = index[1]
    tt1 = time.time()
    products = np.inner(user_vec, vectors) #numpy求user_vec 和 item_vecs的内积
    tt2 = time.time()
    # products_id = sorted(range(len(products)), key=lambda x:products[x], reverse=True) #返回排序后的index
    products_id = np.argsort(-products)[:count]
    #ind = np.argpartition(products, -count)[-count:]
    #products_id = ind[np.argsort(products[ind])]
    tt3 = time.time()
    result = [ids[i] for i in products_id] #返回top count条向量的cid
    tt4 = time.time()
    print('inner product cost:%s, sort cost:%s, return cost:%s ' % (int((tt2-tt1)*1000), int((tt3-tt2)*1000), int((tt4-tt3)*1000)))
    print('topN results : ',result)
    return result

def Traditional2Simplified(sentence):
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

def tag_preprocess(tag):
    #tag格式预处理
    sentline = Traditional2Simplified(tag)
    sentline = sentline.replace('\"', '').replace('#', '').replace('”', '').replace('“', '').replace('、', ',').replace(' ', ',')
    sentline = sentline.lower()
    return sentline

### 4 ### 少tag补全
results = {}
for key in topicMap.keys():
    if len(topicMap[key]) < 3:
        print('******'*5)
        print(key, topicMap[key])
        tmpTags = topicMap[key]
        tmpVecs = []
        
        for tag in tmpTags:
            try:
                #tag = tag.decode('utf-8')
                sentline = Traditional2Simplified(tag)
                #sentline = sentline.encode('utf-8')
                sentline = sentline.replace('\"', '').replace('#', '').replace('”', '').replace('“', '').replace('、', ',').replace(' ', ',')
                sentline = sentline.lower()
                #tag = sentline.decode('utf-8')           
                vec = tagVec[tagName.index(sentline)]
                tmpVecs.append(vec)
            except Exception as e:
                print(e)
                continue
                
        if len(tmpVecs) == 0:
            continue
        tmpVecs = np.array(tmpVecs, dtype=np.float64)
        tmpVecs = np.sum(tmpVecs, axis=0)
        print('vector : ', tmpVecs)    
        tmpResult = search_vectors(tmpVecs, 10, indexs)
        #print(result)
        results[key] = tmpResult

with open ('tagAppendix.txt','w') as f:
    for k in results.keys():
        v = results[k]
        f.write(str(k) + '\t' + str(v) + '\n')

print('done')

### 5 ### 获取每个主题所对应的向量






