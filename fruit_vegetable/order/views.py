import json
import datetime
from django.db import transaction
from django.http import JsonResponse, HttpResponse

from django.conf import settings
# Create your views here.
from django.views import View
from django.utils.decorators import method_decorator

from carts.views import CartsView
from pay.views import JumpView
from tools.logging_dec import logging_check

from user.models import Address

from order.models import OrderGoods, Orderinfo
from goods.models import GoodsInfo

class AdvanceOrderView(View):

    @logging_check
    def get(self,request,username):

        settlement_type = request.GET.get('settlement_type')
        if not settlement_type:
            return JsonResponse({'code': 10500, 'error': 'Please give me type'})
        settlement_type = int(settlement_type)

        user = request.myuser
        address_list = self.get_addrss(user.id)
        #查询字符串 -> settlement_type  0购物车
        if settlement_type == 0:
            # 购物车
            # 购物车中选中商品的数据
            sku_list = self.get_order_carts_list(user.id)
        else:
            # 直接购买
            sku_list=[]
        data={}

        data['addresses']=address_list
        data['sku_list']=sku_list






        #地址： 默认地址在数组的最前方[即0号索引位]
        #sku_list: 只显示购物车中选中的商品对应的信息

        return JsonResponse({'code':200, 'data':data,"base_url":settings.PIC_URL })
    #获取地址
    def get_addrss(self, username):
        all_address = Address.objects.filter(is_active=True, username=username)
        default_address = []
        no_default_address = []
        for addr in all_address:
            addr_dict = {}
            addr_dict['id'] = addr.id
            addr_dict['name'] = addr.receiver
            addr_dict['mobile'] = addr.receiver_mobile
            addr_dict['title'] = addr.tag
            addr_dict['address'] = addr.address
            if addr.is_default:
                default_address.append(addr_dict)
            else:
                no_default_address.append(addr_dict)

        return default_address + no_default_address
    #总金额
    # def get_buy_count(self,sku_list):
    #     buy_count=0
    #     for sku in sku_list:
    #         count=int(sku['count'])
    #         price=int(sku['price'])
    #         buy_count +=count * price
    #     return buy_count

    def get_order_carts_list(self, username):
        # 购物车数据
        carts_obj = CartsView()
        sku_list = carts_obj.get_carts_list(username)
        return [s for s in sku_list if s['selected'] == 1]


class OrderInfoView(View):

    def get_carts_order_data(self, uid):

        carts_obj = CartsView()
        # carts_1 - {'sku_id':[count, select]}
        all_data = carts_obj.get_carts_datas(uid)

        return {k:v for k, v in all_data.items() if v['selected'] == 1}


    @logging_check
    def post(self, request, username):

        user = request.myuser
        json_str = request.body
        json_obj = json.loads(json_str)
        address_id = json_obj.get('address_id')


        #TODO
        #直接购买进入，则多出 sku相关参数

        #检查地址
        try:
            address = Address.objects.get(username=user.id, id=address_id, is_active=True)
        except Exception as e:
            return JsonResponse({'code':10501, 'error':'The address is error'})

        # 插入订单数据
        # 订单商品数据
        # SKU数据 update
        with transaction.atomic():
            sid = transaction.savepoint()
            #生成订单号
            now = datetime.datetime.now()
            order_id = '%s%0.2d'%(now.strftime('%Y%m%d%H%M%S'), user.id)

            total_amount = 0
            total_count = 0
            order = Orderinfo.objects.create(
                order_id = order_id,
                user_info = user,
                address = address.address,
                receiver = address.receiver,
                receiver_mobile = address.receiver_mobile,
                tag = address.tag,
                total_amount = total_amount,
                total_count = total_count,
                freight = 10,
                pay_method = 1,
                status = 1
            )

            #取购物车数据
            carts_dict = self.get_carts_order_data(user.id)
            skus = GoodsInfo.objects.filter(id__in=carts_dict.keys())

            #检查库存、是否上架/ 修改库存 / 创建订单商品数据
            #删除购物车选中商品
            #transaction.savepoint_rollback(sid)
            for sku in skus:
                if not sku.is_active:
                    continue
                carts_count = carts_dict[sku.id]['count']
                if carts_count > sku.stock:
                    #回滚
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'code':10503, 'errmsg':'商品%s库存不足'%(sku.name)})


                result = GoodsInfo.objects.filter(id=sku.id,).update(stock=sku.stock - carts_count, sales=sku.sales + carts_count)
                if result == 0:
                    #库存发生变化
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'code':10504, 'errmsg':'The server is busy'})

                OrderGoods.objects.create(
                    order_info = order,
                    good_info = sku,
                    number = carts_count,

                )

                total_count += carts_count
                total_amount += sku.price * carts_count

            order.total_count = total_count
            order.total_amount = total_amount
            order.save()


            #提交事务
            transaction.savepoint_commit(sid)

        #Todo 删除购物车中选中的商品
        pay_money=order.total_amount + order.freight
        pay=JumpView()
        pay_url=pay.post(request,order_id,str(pay_money))
        for sku in skus:
            delet=CartsView()
            delet.del_carts_data(user.id,sku.id)
        data = {
            'saller': '996水果商城',
            'total_amount': pay_money,
            'order_id': order_id,
            'pay_url': pay_url,
            'carts_count': 0 #购物车删除方法返回该值
        }

        return JsonResponse({'code':200, 'data':data})

    @logging_check
    def get(self, request, username):
        user = request.myuser
        type = request.GET.get('order_status')
        print("*" * 100)
        print(user.username)
        if type == 0:
            try:
                orderinfo_list = Orderinfo.objects.filter(username=user.username)
            except Exception as e:
                print("*" * 100)
                return JsonResponse({"code": 304})
        else:
            try:
                orderinfo_list = Orderinfo.objects.filter(username=user.username, status=type)
            except Exception as e:
                print("*" * 100)
                return JsonResponse({"code": 304})
        print("^" * 100)

        order_list = self.get_order_info(orderinfo_list)
        data = {}
        data['orders_list'] = order_list
        result = {"code": 200, "data": data}
        return JsonResponse(result)

    def get_order_info(self, orderinfo_list):
        order_list = []
        for order in orderinfo_list:
            order_dict = {}
            order_dict["order_id"] = order['order_id']
            order_id = order['order_id']
            order_dict['order_total_count'] = order["total_count"]
            order_dict['order_total_amount'] = order["total_amount"]
            order_dict['order_freight'] = order["freight"]
            order_dict['address'] = {}
            order_dict['address']['title'] = order['tag']
            order_dict['address']['address'] = order['address']
            order_dict['address']['receiver_mobile'] = order['receiver_mobile']
            order_dict['address']['receiver'] = order['receiver']
            order_dict["status"] = order["status"]
            order_dict["order_sku"] = OrderGoods.objects.filter(order_info_id=order_id)
            order_dict["order_time"] = order["created_time"]
            order_list.append(order_dict)

        return order_list

    @logging_check
    def put(self, request, username):
        user = request.myuser
        json_str = request.body
        json_obj = json.loads(json_str)
        order_id = json_obj.get('order_id')
        try:
            order = Orderinfo.objects.get(order_id=order_id)
        except Exception as e:
            return JsonResponse({"code": 100304})
        print(order)
        order['status'] = 4
        order.save()
        return JsonResponse({"code": 200})


