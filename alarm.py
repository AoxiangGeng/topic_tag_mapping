# -*- coding: UTF-8 -*-

import argparse

import requests
import json


class Alarm(object):

    def __init__(self, args):
        self.url = "http://sender.office.bbobo.com"

        self.body = {"app_token": "0hlYDkPaqAwwvFvv", "send_type": "ESWD", "level": "WARNING", "service_name": "候选集处理流程"}
        self.subject = args.subject
        self.content = args.content
        if args.mail:
            self.body['email_to'] = args.mail.split(',')
        if args.mobile:
            self.body['mobile_to'] = args.mobile.split(',')
        if args.wechat:
            self.body['wechat_to'] = args.wechat.split(',')

        self.body['subject'] = self.subject
        self.body['content'] = self.content

    def alarm(self):
        print(self.body)
        headers = {'Content-Type': 'application/json'}
        res = requests.post(self.url, data=json.dumps(self.body), headers=headers)
        print res


def main():
    parser = argparse.ArgumentParser(
        description="python alarm.py --subject='候选集subject' --content='test' --mail='gengaoxiang@yixia.com' --mobile='13693387809'  --wechat='gengao1991'")

    parser.add_argument('--subject', type=str, default='候选集报警')
    parser.add_argument('--content', type=str, default="WARNING")
    parser.add_argument('--mail', type=str, default=None)
    parser.add_argument('--mobile', type=str, default=None)
    parser.add_argument('--wechat', type=str, default=None)

    args = parser.parse_args()
    # print args
    alarm = Alarm(args)

    alarm.alarm()


if __name__ == '__main__':
    main()