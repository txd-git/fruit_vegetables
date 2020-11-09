from django.db import models
from user.models import UserInfo
from goods.models import GoodsInfo
chice_toulp=(
    (1,'待付款'),
    (2,'待发货'),
    (3,'待收货'),
    (4,'已收货')
)
# Create your models here.
class Orderinfo(models.Model):
    order_id= models.CharField(verbose_name="订单号",max_length=64,primary_key=True)
    # paytipy=models.
    total_count=models.IntegerField('订单数目',default=1)
    total_amount=models.DecimalField('商品总价格',max_digits=10,decimal_places=2)
    freight=models.DecimalField('运费',max_digits=10,decimal_places=2)
    pay_method=models.SmallIntegerField('支付方式',default=1,)
    receiver=models.CharField('收件人',max_length=11,default='')
    address=models.CharField('收货地址',max_length=100,default='')
    receiver_mobile=models.CharField('收件人电话',max_length=11)
    tag=models.CharField('标签',max_length=11,default='')
    status=models.SmallIntegerField('订单状态',choices=chice_toulp)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now_add=True)

    class Meta:
        db_table='orderInfo'
    def __str__(self):
        return self.order_id


class OrderGoods(models.Model):
    number=models.IntegerField('购买数量',default=1)
    good_info = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE)
    order_info = models.ForeignKey(Orderinfo, on_delete=models.CASCADE)
    class Meta:
        db_table='orderGoods'