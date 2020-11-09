from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruit_vegetable.settings')
# 2.创建app(Celery对象)
app = Celery('fruit_vegetable')
# 3再配置
app.conf.update(
    BROKER_URL='redis://@127.0.0.1:6379/1'
)
# 4告知celery去那个应用下找任务函数
app.autodiscover_tasks(settings.INSTALLED_APPS)