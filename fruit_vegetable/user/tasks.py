from django.conf import settings
from fruit_vegetable.celery import app
from tools.sms import YunTongXin


@app.task
def send_sms(phone,code):
    x=YunTongXin(settings.SMS_ACCOUNT_ID,settings.SMS_ACCOUNT_TOKEN,settings.SMS_APP_ID,settings.SMS_TEMPLATES)
    print('send_sms')
    res=x.run(phone,code)
    return res

