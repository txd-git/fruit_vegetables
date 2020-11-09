from django.shortcuts import render

# Create your views here.

import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from alipay import AliPay
from django.conf import settings
# Create your views here.
from django.views import View
ORDER_STATUAS=1
app_private_key_string=open(settings.ALIPAY_KEY_DIR+'app_private_key.pem').read()
alipay_public_key_string=open(settings.ALIPAY_KEY_DIR+'alipay_public_key.pem').read()
class MyAlipay(View):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.alipay=AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type='RSA2',
            debug=True,
        )
    def get_trade_url(self,order_id,amount):

        base_url='https://openapi.alipaydev.com/gateway.do'
        order_string=self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=amount,
            subject=order_id,
            return_url=settings.ALIPAY_RETURN_URL,
            NOTIFY_URL=settings.ALIPAY_NOTIFY_URL
        )
        return base_url+'?'+order_string
    def get_trade_result(self,order_id):
        result=self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        if result.get('trade_status')=='TRADE_SUCCESS':
            return True
        return False

class JumpView(MyAlipay):
    def post(self,request,order_id,pay_money):
        pay_url=self.get_trade_url(order_id,pay_money)
        return pay_url


    def get(self,request):

        return render(request,'ajax_alipay.html')



class ResultView(MyAlipay):
    def get(self,request):
        request_data = {k: request.GET(k) for k in request.POST.keys()}
        print('--------------request_data------------')
        print(request_data)
        order_id=request_data['out_trade_no']
        if ORDER_STATUAS==1:
            #证明post有bug,需要我们主动向支付宝查询
            result=self.get_trade_result(order_id)
            if result:
                return HttpResponse('支付成功')
            return HttpResponse('支付失败')
            pass
        return HttpResponse('diaohui')
    def get_verify_result(self,data,sign):
        return self.alipay.verify(data,sign)
    def post(self,request):
        #支付完成后,post对应的url是ALIPAY_NOTIFY_URL[带支付信息]
        #支付宝服务器发送过来的数据转化为标准的python字典
        request_data={k:request.POST[k] for k in request.POST.keys()}
        #取出数据中的签名
        sign=request_data.pop('sign')

        is_verify=self.get_verify_result(request_data,sign)
        if is_verify:
            #取出交易订单
            trade_status=request_data['trade_status']
            #将数据库的订单状态修改为支付成功
            if trade_status=='TRADE_SUCCESS':
                return HttpResponse('ok')
            else:
                # 将数据库的订单状态修改为支付成功
                return HttpResponse('error')
        else:
            return HttpResponse('非法访问')
