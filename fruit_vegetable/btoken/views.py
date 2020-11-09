import hashlib
import json

from django.http import JsonResponse
from django.shortcuts import render
from user.models import UserInfo
# Create your views here.
from django.views import View
from user.views import make_token, get_token
from order.models import Orderinfo


class TokenViews(View):
    def post(self, request):
        # tokens=request.META.get('HTTP_AUTHORIZATION')
        # print(tokens)
        # name=get_token(tokens.encode())['username']
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        password = json_obj['password']
        print(password)
        # if name==username:
        #     return JsonResponse({'code':204,'error':"您已经登陆过了"})
        try:
            user = UserInfo.objects.get(username=username)
        except:
            result = {'code': 201, 'error': 'username is not exist'}
            return JsonResponse(result)
        md5 = hashlib.md5()
        md5.update(password.encode())
        password_m = md5.hexdigest()
        print(password_m)
        token = make_token(username)
        print(token)
        print(user.password)
        if password_m == user.password:
            num = 0
            result = {'code': 200, 'username': username, 'data': {'token': token.decode(), 'carts_count': num}}
            return JsonResponse(result)
        return JsonResponse({'code': 201, 'error': '密码错误'})
