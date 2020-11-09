import base64
import datetime
import hashlib
import json

import requests


class YunTongXin:
    base_url='https://app.cloopen.com:8883'
    def __init__(self, accountSid,accountToken,appId,templateId):
        self.accountSid=accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId
    def get_request_url(self,sig):
        self.url=self.base_url+'/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s'%(self.accountSid,sig)
        return self.url
    def get_timestamp(self):
        print('get_timestamp')
        now=datetime.datetime.now()
        now_str=now.strftime('%Y%m%d%H%M%S')
        return now_str
    def get_sig(self,timestamp):
        print('get_sig')
        s=self.accountSid+self.accountToken+timestamp
        md5=hashlib.md5()
        md5.update(s.encode())
        return md5.hexdigest().upper()
    def get_request_header(self,timestamp):
        print('get_request_header')
        s=self.accountSid+':'+timestamp
        b_s=base64.b64encode(s.encode()).decode()
        return {
            'Accept':'application/json',
            'Content-Type':'application/json;charset=utf-8',
            'Authorization':b_s
        }
    def get_request_body(self,phone,code):
        print('get_request_body')
        data={
            'to':phone,
            'appId':self.appId,
            'templateId':self.templateId,
            'datas':[code,'3']

        }
        return data
    def do_request(self,url,header,body):
        print('do_request')
        res=requests.post(url,headers=header,data=json.dumps(body))
        return res.text
    def run(self,phone,code):
        timestamp=self.get_timestamp()
        sig=self.get_sig(timestamp)
        url=self.get_request_url(sig)
        header=self.get_request_header(timestamp)
        body=self.get_request_body(phone,code)
        res=self.do_request(url,header,body)
        return res
# if __name__ == '__main__':
#     aid='8aaf0708732220a6017439649d7c7758'
#     atoken='b1db318d489741b2a151f4a83e2e5caf'
#     appid='8aaf0708732220a6017439649e4b775e'
#     tid=1
#     x=YunTongXin(aid,atoken,appid,tid)
#     res=x.run('13289333637','654321')
#     print(res)
