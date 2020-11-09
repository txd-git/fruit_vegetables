from django.contrib import admin
from .models import GoodsInfo,GoodsCatalog
# Register your models here.
class GoodsInfoManage(admin.ModelAdmin):
    list_display = ['id','name','cost_price','price','origin_place','stock','sales','image_url','is_active','comm_class']
    list_filter=['stock','comm_class','sales']
    search_fields=['name','comm_class']
class GoodsCatalogManage(admin.ModelAdmin):
    list_display = ['id','name']
admin.site.register(GoodsInfo,GoodsInfoManage)
admin.site.register(GoodsCatalog,GoodsCatalogManage)