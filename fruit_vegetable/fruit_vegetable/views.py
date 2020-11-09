import json

from django.conf import settings

from django.http import JsonResponse

from django.core.cache import cache

from goods.models import GoodsInfo


def pwfind(request):
    user_str = request.body
    user_obj = json.loads(user_str)
    code = user_obj['code']
    phone = user_obj['phone']
    cache_key = 'sms_%s' % phone
    old_code = cache.get(cache_key)
    if not old_code:
        result = {'code': 201, 'error': {'message': '验证码失效'}}
        return JsonResponse(result)
    if old_code != code:
        result = {'code': 202, 'error': {'message': '验证码错误'}}
        return JsonResponse(result)
    result = {'code': 200, }
    return JsonResponse(result)
