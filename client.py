# -*- coding: utf-8 -*-
import json
import requests

topic_url = "http://10.0.8.45:10886/get_video_topics"

headers = {'content-type': 'application/json'}
tags = ['連名帶姓', 'A-mei', 'Amei', '偷故事的人', '伍芝儀', 'Ariane', '翻唱', '連名帶姓翻唱', 'A-mei翻唱', 'Amei翻唱', '連名帶姓Cover', 'Cover', 'AmeiCover', '偷唱歌的人']

data = {'tags':tags, 'count':5}
res = requests.post(topic_url, data=json.dumps(data),\
                              headers=headers)

print(res.json())
