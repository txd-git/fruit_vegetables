from django.contrib import admin
from .models import UserInfo,Address

# Register your models here.
class UserInfoManage(admin.ModelAdmin):
    list_display = ['id','username','phone','email','password','created_time','updated_time']
    list_filter = ['username','created_time','updated_time']
    search_fields = ['username','updated_time','created_time']
class AddressManage(admin.ModelAdmin):
    list_display = ['id','receiver','receiver_mobile','address','postcode','tag','is_default','is_active','username']
admin.site.register(UserInfo,UserInfoManage)
admin.site.register(Address,AddressManage)
