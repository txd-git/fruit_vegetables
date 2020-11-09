import jwt
from django.http import JsonResponse
from django.conf import settings
from user.models import UserInfo

def logging_check(func):

    def wrapper(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code':403, 'error': 'Please login'}
            return JsonResponse(result)

        try:
            res = jwt.decode(token,settings.JWT_TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            print('jwt decode error is %s'%(e))
            result = {'code':403, 'error': 'Please login'}
            return JsonResponse(result)

        username = res['username']

        user = UserInfo.objects.get(username=username)
        request.myuser = user
        # print(request.myuser.username)

        return func(self, request, *args, **kwargs)

    return wrapper

