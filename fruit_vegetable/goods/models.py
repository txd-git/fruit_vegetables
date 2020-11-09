from django.db import models


# Create your models here.
class GoodsCatalog(models.Model):
    name = models.CharField('商品种类', max_length=20)

    class Meta:
        db_table = 'goodsCatalog'

    def __str__(self):
        return self.name


class GoodsInfo(models.Model):
    name = models.CharField('商品名称', max_length=20, unique=True)
    cost_price = models.DecimalField('进价', max_digits=5, decimal_places=2)
    price = models.DecimalField('单价', max_digits=5, decimal_places=2)
    origin_place = models.CharField('产地', max_length=30)
    stock = models.IntegerField('库存', default=0)
    sales = models.IntegerField('销量', default=0)
    image_url = models.ImageField(verbose_name="图片路径", default=None, upload_to="comm_img")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now_add=True)
    is_active = models.BooleanField('是否上架', default=True)
    comm_class = models.ForeignKey(GoodsCatalog, on_delete=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goodsInfo'
