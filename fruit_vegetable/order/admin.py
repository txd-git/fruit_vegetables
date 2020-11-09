from django.contrib import admin
from .models import Orderinfo
# Register your models here.

class OrderinfoManage(admin.ModelAdmin):
    list_display = ['name', 'order_id', 'total_count', 'total_amount', 'freight', 'pay_method', 'receiver', 'address','receiver_mobile','tag','status','user_info',]
    list_filter = ['name', 'user_info',]
    search_fields = ['name', 'user_info']

admin.site.register(Orderinfo,OrderinfoManage)
