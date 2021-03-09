#!bin/bash
set hive.execution.engine=tez;

dt=`date +"%Y%m%d" -d "1 day ago"`
hour=`date -d  '2 hour ago'  +'%H'`

hive -e "
set hive.auto.convert.join = false;
SELECT topic_id, bind_uid, bind_name
    FROM dim_bobo.dim_bobo_topic_user_bind_hour 
    WHERE use_status = 1 
        AND sync_status = 2
" > /data/ylzhang/for_newauthor_yy/topic_tag_mapping/author_topics.txt
        
wc -l /data/ylzhang/for_newauthor_yy/topic_tag_mapping/author_topics.txt
