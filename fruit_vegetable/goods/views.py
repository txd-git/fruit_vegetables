from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
# Create your views here.
from django.views import View
from goods.models import GoodsInfo
from django.core.paginator import Paginator


class GoodsDetailView(View):
    def get(self, request, goodsid):
        print('delail in----')
        """
        :param type:
        :param id:
        :return:
        """
        sku_details = {}
        # 查找类型的商品
        sku_item = GoodsInfo.objects.get(id=goodsid)
        sku_catalog = sku_item.comm_class
        # 生成前端所需要的数据
        sku_details['image'] = str(sku_item.image_url)
        sku_details["spu"] = sku_item.id
        sku_details["name"] = sku_item.name
        sku_details["caption"] = None
        sku_details["price"] = str(sku_item.price)
        sku_details["catalog_id"] = sku_catalog.id
        sku_details["catalog_name"] = sku_catalog.name
        result = {'code': 200, 'data': sku_details, 'base_url': settings.PIC_URL}
        return JsonResponse(result)


class GoodsListView(View):
    def get(self, request, type):
        page_num = int(request.GET.get('page', 1))
        sku_list = GoodsInfo.objects.filter(comm_class=type, is_active=True)
        page_size = 3
        try:
            # 对商品进行分页处理
            paginator = Paginator(sku_list, page_size)
            page_skus = paginator.page(page_num)
            # 构造商品列表
            page_skus_json = []
            for sku in page_skus:
                # 生成商品信息,并将商品信息添加到列表中
                sku_dict = {}
                sku_dict['skuid'] = sku.id
                sku_dict['name'] = sku.name
                sku_dict['price'] = str(sku.price)
                sku_dict['image'] = str(sku.image_url)
                page_skus_json.append(sku_dict)
        except:
            result = {'code': 40200, 'error': '已经是最后一页了'}
            return JsonResponse(result)
        result = {'code': 200, 'data': page_skus_json, 'paginator': {'pagesize': page_size, 'total': len(sku_list)},
                  'base_url': settings.PIC_URL}
        return JsonResponse(result)
