#!/bin/bash
. /etc/profile
set -v
#used for download trained model to local
curr_day=$1
basedir=`dirname $0`
if [ "$basedir" = "." ]
then
    basedir=`pwd`
else
    cd $basedir
fi
echo ${basedir} #/data/aoxiang

if [ "\$$curr_day" = "$" ]; then
    curr_day=`date +%Y%m%d`;
else
    curr_day=`date -d "$curr_day" +%Y%m%d`
fi

YESTERDAY=`date -d "$curr_day -1 day" +%Y%m%d`;
echo ${YESTERDAY}


project_dir="/data/ylzhang/for_newauthor_yy/topic_tag_mapping" #/data/aoxiang/yt-rec-ffm-recall
alarm_py="${project_dir}/alarm.py"
python3path="/home/jms_su2root/anaconda3/bin/python3"
python2path="/usr/bin/python2"


#检查样本数据
author_topic_count=`cat ${project_dir}/author_topics.txt |wc -l `
echo 'author_topic_count : ', $author_topic_count
if [ $author_topic_count -lt 100 ]; then
    echo '主题绑定作者数据出错'
    $python2path $alarm_py    --subject='8.45 主题绑定作者数据出错'    --content='8.45 主题预测服务绑定作者数据出错'   --mobile='13693387809' --wechat='gengaoxiang'
    exit 1
fi

#重启主服务
ps aux|grep 'python3 -u topic_server.py'|awk '{print $2}'|xargs -i kill -9 {}
nohup python3 -u topic_server.py > nohup.out 2>&1 &

echo 'ALL SUCCEED'




