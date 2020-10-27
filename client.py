# -*- coding: utf-8 -*-
import json
import requests

topic_url = "http://10.0.8.45:10986/get_video_topics"

headers = {'content-type': 'application/json'}
tags = ['連名帶姓', 'A-mei', 'Amei', '偷故事的人', '伍芝儀', 'Ariane', '翻唱', '連名帶姓翻唱', 'A-mei翻唱', 'Amei翻唱', '連名帶姓Cover', 'Cover', 'AmeiCover', '偷唱歌的人']
tags = ['找蔬食', '素食拌麵', '乾拌麵', '開箱', '蔬食', '素食youtuber', 'traveggo', '找蔬食traveggo', '千千', '美食水水', '水哦', '千拌麵', '賈以食日', '鋒味拌麵', '賈靜雯', '謝霆鋒', '曾拌麵', '拌麵', 'KIKI拌麵']
data = {'tags':tags, 'count':5, 'author':'587137364747484225'}
res = requests.post(topic_url, data=json.dumps(data),\
                              headers=headers)

print(res.json())
