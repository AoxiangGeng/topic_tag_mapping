# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import os
import numpy as np
import time
from langconv import *
import re
import sys
import random
import json
from collections import defaultdict
import requests
import pickle
import logging

#################
# 视频主题预测服务 #
#################

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(process)d - %(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info('Start loading models! ')

app = Flask(__name__)

class video_topics_helper():
    def __init__(self):
        #initialization
        self.tagName, self.tagVec = self.load_vectors()
        self.topic_index = self.load_topic_pkl()
        self.topics = self.topic_index[0]
        self.author_topic_map = self.load_censored_authors()
        logger.info('initialization done \n')

    def load_vectors(self):
        #加载所有词向量
        tagName = []
        tagVec = []
        count = 0
        for i in range(0,50):
            with open ('./vectors_append/part-000%02d'%i, 'r') as f:
                logger.info('./vectors_append/part-000%02d'%i)
                for line in f.readlines():
                    tag = line.strip().split('\t')[0]
                    vec = line.strip().split('\t')[2].split(',')
                    vec = np.array(vec, dtype=np.float64)
                    tagVec.append(vec)
                    tagName.append(tag)
                    count += 1
                    # if count % 100000 == 0:
                    #     print(count, tag)
        logger.info('length of tag %d, vectors %d' % (len(tagName),len(tagVec)))
        return tagName, tagVec

    def load_topic_pkl(self):
        #加载每个主题的向量
        file = open('./data/topicVectors.pkl','rb')
        topic_index = pickle.load(file)
        file.close()
        return topic_index

    def load_censored_authors(self):
        #加载运营标注垂类主题的作者id
        topic_author_map = {}
        index = 0
        with open ('./data/censored_authors.csv','r') as f:
            for line in f.readlines():
                index += 1
                if index == 1 : continue
                category = line.strip().split(',')[0]
                topic = line.strip().split(',')[1]
                authors = [item for item in line.strip().split(',')[2:] if item != '']
                topic_author_map[topic] = authors
        
        author_topic_map = defaultdict(list)
        for topic,authors in topic_author_map.items():
            for author in authors:
                author_topic_map[author].append(topic)
        del topic_author_map
        return author_topic_map

    def result_post_process(self, author, result, count):
        #对结果进行后处理，如果作者id存在于author_topic_map中，则将author_topic_map中该作者对应的主题添加在结果前列
        appendix = self.author_topic_map.get(author,[])
        result = appendix + result
        return result[:count]

    def search_vectors(self, user_vec, count, index):
        #暴力计算返回内积结果最大的向量
        ids = index[0]
        vectors = index[1]
        products = np.inner(user_vec, vectors) #numpy求user_vec 和 item_vecs的内积
        # products_id = sorted(range(len(products)), key=lambda x:products[x], reverse=True) #返回排序后的index
        products_id = np.argsort(-products)[:count]
        result = [ids[i] for i in products_id]
        #ind = np.argpartition(products, -count)[-count:]
        #products_id = ind[np.argsort(products[ind])]
        # logger.info('top results : ' + str(result))
        return result

    def Traditional2Simplified(self, sentence):
        #繁体转换
        sentence = Converter('zh-hans').convert(sentence)
        return sentence

    def tag_preprocess(self, tag):
        #tag格式预处理
        sentline = self.Traditional2Simplified(tag)
        sentline = sentline.replace('\"', '').replace('#', '').replace('”', '').replace('“', '').replace('、', ',')
        sentline = sentline.lower()
        return sentline

    def querry(self, tags, count):
        #向量搜索
        tmpVecs = []
        tmpTags = [self.tag_preprocess(i) for i in tags]
        for tag in tmpTags:
            try:
                vec = self.tagVec[self.tagName.index(tag)]
                tmpVecs.append(vec)
            except Exception as e:
                continue
        #如果所有tag都没有找到对应向量，随机返回topic
        if len(tmpVecs) == 0:
            logger.warning('无匹配词向量')
            result = random.sample(self.topics, count)
            return result
        tmpVecs = np.array(tmpVecs, dtype=np.float64)
        tmpVecs = np.sum(tmpVecs, axis=0) / len(tmpVecs)   
        result = self.search_vectors(tmpVecs, count, self.topic_index)
        return result

#加载工具类
topicHelper = video_topics_helper()

#FLASK server 
@app.route('/get_video_topics', methods=['POST'])
def get_video_ids():

    try:
        #从实时的request中获取信息
        req = request.json
        logger.info(str(req))
        tags = req['tags']
        count = req['count']
        try:
            author = str(req['author'])
        except:
            author = '666'
        result = topicHelper.querry(tags, count)
        result = topicHelper.result_post_process(author, result, count) #后处理
        if len(result) == 0:
            logger.warning('### 返回为空 ###')
            return Response(response=json.dumps([]), status=200, mimetype="application/json")
        logger.info("result return to client: " + str(result))

    except Exception as e:
        #出现异常，status=300
        logger.error('### 返回异常 ###', e)
        logger.error('api:%s', e)
        return Response(response=json.dumps([]), status=300, mimetype="application/json")

    #结果正常，status=200
    return Response(response=json.dumps(result), status=200, mimetype="application/json")



if __name__ == '__main__':
    #启动FLASK服务(非高并发模式)
    #app.run(host="127.0.0.1", port=18901) #, debug=False, threaded=False)
    #启动FLASK服务--多线程模式
    # app.run(host="0.0.0.0", port=10986, debug=False, threaded=True)
    #启动FLASK服务--多进程模式
    app.run(host="0.0.0.0", port=10986, debug=False, threaded=False, processes=5)




