import hashlib
import random
import time

import jwt
from django.core.cache import cache
from django.views import View

from user.tasks import send_sms
from .models import UserInfo, Address
from django.conf import settings
from order.models import Orderinfo
import json
from tools.logging_dec import logging_check

from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
class AddUser(View):

    # 注册
    def post(self, request):
        data = request.body
        data_obj = json.loads(data)
        username = data_obj['uname']
        password = data_obj['password']
        phone = data_obj['phone']
        email = data_obj['email']
        if not phone:
            return JsonResponse({'code': 10210, 'error': "请填写手机号"})
        if len(username) > 11 and len(username) < 6:
            result = {'code': 10100, 'error': '用户名不符合要求'}
            return JsonResponse(result)
        if len(password) > 11 and len(password) < 6:
            result = {'code': 10101, 'error': '密码不符合要求'}
            return JsonResponse(result)
        try:
            code = int(data_obj['verify'])
        except:
            result = {'code': 202, 'error': {'message': '验证码错误'}}
            return JsonResponse(result)
        cache_key = 'sms_%s' % phone
        old_code = cache.get(cache_key)
        if not old_code:
            result = {'code': 201, 'error': {'message': '验证码失效'}}
            return JsonResponse(result)
        if old_code != code:
            result = {'code': 202, 'error': {'message': '验证码错误'}}
            return JsonResponse(result)
        try:
            old_phone = UserInfo.objects.get(phone=phone)

            result = {'code': 10114, 'error': '手机号已存在'}
            return JsonResponse(result)
        except:
            pass
        md5 = hashlib.md5()
        md5.update(password.encode())
        password_m = md5.hexdigest()

        user = UserInfo.objects.filter(username=username)
        if user:
            result = {'code': 10201, 'error': {'message': 'name is exist'}}
            return JsonResponse(result)

        try:
            UserInfo.objects.create(username=username, phone=phone, email=email, password=password_m)
        except Exception as e:
            print(1)
            result = {'code': 10201, 'error': {'message': 'name is exist'}}
            return JsonResponse(result)

        num = 0
        token = make_token(username)
        result = {'code': 200, 'username': username, 'data': {'token': token.decode(), 'carts_count': num}}
        return JsonResponse(result)


class ChangePwd(View):
    @logging_check
    def post(self, request, username):
        if request.method != 'POST':
            result = {'code': 10105, 'error': '请使用POST'}
            return JsonResponse(result)
        user = request.myuser
        username = user.username
        data = request.body
        data_obj = json.loads(data)
        password_1 = data_obj['password1']
        print(password_1, 'password_1')
        password_2 = data_obj['password2']
        print(password_2, 'password_2')
        old_password = data_obj['oldpassword']
        if not old_password:
            # result = {'code': 10106, 'error': '请输入旧密码'}
            result = {'error': '请输入旧密码'}
            return JsonResponse(result)

        old_user = UserInfo.objects.get(username=username)
        md5 = hashlib.md5()
        md5.update(old_password.encode())
        password_old = md5.hexdigest()
        if password_old != old_user.password:
            result = {'code': 10107, 'error': '旧密码错误，请重新输入'}
            return JsonResponse(result)

        if len(password_1) > 11 and len(password_1) < 6:
            result = {'code': 10101, 'error': '密码不符合要求'}
            return JsonResponse(result)
        if password_1 != password_2:
            result = {'code': 10102, 'error': '两次密码不一致'}
            return JsonResponse(result)
        # 为新密码加密保存入数据库
        md6 = hashlib.md5()
        md6.update(password_1.encode())
        password_n = md6.hexdigest()
        print(password_n)
        user = UserInfo.objects.get(username=username)
        print(user.password)
        user.password = password_n
        user.save()
        user1 = UserInfo.objects.get(username=username)
        print(user1.password)
        result = {'code': 200}

        return JsonResponse(result)


#
def verification(request):
    data = request.body
    data_obj = json.loads(data)
    phone = data_obj['phone']
    old_phone = UserInfo.objects.filter(phone=phone)
    if not old_phone:
        result = {'code': 303, 'error': '手机号码不存在.'}
        return JsonResponse(result)

    try:
        code = int(data_obj['code'])
    except:
        result = {'code': 203, 'error': '验证码错误'}
        return JsonResponse(result)
    cache_key = 'sms_%s' % phone
    old_code = cache.get(cache_key)
    if not old_code:
        result = {'code': 201, 'error': '验证码失效'}
        return JsonResponse(result)
    if old_code != code:
        result = {'code': 202, 'error': {'message': '验证码错误'}}
        return JsonResponse(result)

    return JsonResponse({"code": 200})


#
def findpass(request):
    data = request.body
    data_obj = json.loads(data)
    password1 = data_obj['password1']
    password2 = data_obj['password2']
    phone = str(data_obj['phone'])

    if password1 != password2:
        result = {'code': 301, 'error': '两次密码错误'}
        return JsonResponse(result)
    if len(password1) > 11 or len(password2) < 6:
        result = {'code': 302, 'error': '密码长度不正确'}
        return JsonResponse(result)
    md5 = hashlib.md5()
    md5.update(password1.encode())
    password_m = md5.hexdigest()
    print(password_m)
    try:
        user = UserInfo.objects.get(phone=phone)
        user.password = password_m
        user.save()
    except Exception as e:

        result = {'code': 201, 'error': '手机号错误'}
        return JsonResponse(result)
    return JsonResponse({'code': 200})


class AddressView(View):
    @logging_check
    def post(self, request, username):
        # /v1/users/<username>/address
        """新建地址"""
        json_str = request.body
        json_obj = json.loads(json_str)
        receiver = json_obj['receiver']
        receiver_phone = json_obj['receiver_phone']
        address = json_obj['address']
        postcode = json_obj['postcode']
        tag = json_obj['tag']

        user = request.myuser
        old_address = Address.objects.filter(username=user, is_active=True)
        is_default = False
        if not old_address:
            is_default = True

        Address.objects.create(
            username=user,
            receiver=receiver,
            address=address,
            receiver_mobile=receiver_phone,
            postcode=postcode,
            tag=tag,
            is_default=is_default
        )
        return JsonResponse({'code': 200, 'data': '添加地址成功!'})

    @logging_check
    def get(self, request, username):
        # /v1/users/<username>/address
        """查看地址"""
        all_address = Address.objects.filter(username=request.myuser, is_active=True)
        address_list = []
        for add in all_address:
            add_data = {}
            add_data['id'] = add.id
            add_data['address'] = add.address
            add_data['receiver'] = add.receiver
            add_data['receiver_mobile'] = add.receiver_mobile
            add_data['tag'] = add.tag
            add_data['postcode'] = add.postcode
            add_data['is_default'] = add.is_default
            address_list.append(add_data)
        return JsonResponse({'code': 200, "addresslist": address_list})

    @logging_check
    def put(self, request, address_id, username):
        # /v1/users/<username>/address/<address_id>
        """修改地址"""
        json_str = request.body
        json_obj = json.loads(json_str)
        receiver = json_obj['receiver']
        address = json_obj['address']
        tag = json_obj['tag']
        receiver_mobile = json_obj['receiver_mobile']
        receiver_id = json_obj['id']

        # user = request.myuser
        old_address = Address.objects.filter(id=address_id, is_active=True)
        for add in old_address:
            add.id = receiver_id
            add.receiver = receiver
            add.address = address
            add.tag = tag
            add.receiver_mobile = receiver_mobile
            add.save()
        return JsonResponse({'code': 200, 'data': '修改地址成功!'})

    @logging_check
    def delete(self, request, username, address_id):
        # /v1/users/<username>/address/<address_id>
        """删除地址"""
        json_str = request.body
        json_obj = json.loads(json_str)
        address_id = json_obj['id']
        username = request.myuser
        old_address = Address.objects.filter(username=username, id=address_id, is_active=True)
        for addr in old_address:
            addr.is_active = False
            addr.save()

        return JsonResponse({'code': 200, 'data': '删除成功!'})


class AddressDefaultView(View):
    @logging_check
    def post(self, request, username):
        """设置默认地址"""
        json_str = request.body
        json_obj = json.loads(json_str)
        address_id = json_obj['id']
        username = request.myuser
        addresses = Address.objects.filter(username=username, is_active=True)
        for addr in addresses:

            if addr.is_default:
                addr.is_default = False
                addr.save()
        old_address = Address.objects.get(username=username, id=address_id, is_active=True)
        old_address.is_default = True
        old_address.save()

        return JsonResponse({'code': 200, 'data': '设置成功!'})


def make_token(uname, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'username': uname, 'exp': now + expire}
    return jwt.encode(payload, key, algorithm='HS256')


def get_token(token):
    key = settings.JWT_TOKEN_KEY
    return jwt.decode(token, key, algorithm='HS256')


def sms_send(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    phone = json_obj['phone']
    print(phone)
    cache_key = 'sms_%s' % phone
    old_code = cache.get(cache_key)
    if old_code:
        result = {'code': 10112, 'error': {'message': '验证码已发送'}}
        return JsonResponse(result)
    code = random.randint(1000, 9999)
    print(code)
    cache.set(cache_key, code, 65)
    send_sms.delay(phone, code)
    return JsonResponse({'code': 200})
