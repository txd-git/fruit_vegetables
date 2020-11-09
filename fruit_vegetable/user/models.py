from django.db import models

# Create your models here.



class UserInfo(models.Model):

    username = models.CharField('用户名', max_length=11,unique=True)
    phone= models.CharField('手机',max_length=11,default='')
    email=models.EmailField('邮箱')
    password = models.CharField('密码', max_length=32)

    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    updated_time = models.DateTimeField('更新时间',auto_now=True)
    def __str__(self):
        return self.username
    class Meta:
        db_table='userInfo'
class Address(models.Model):
    receiver=models.CharField('收件人',max_length=10)
    receiver_mobile=models.CharField('联系电话',max_length=11)
    address=models.CharField('收件地址',max_length=100)
    postcode=models.CharField('邮编',max_length=10)
    tag=models.CharField('标签',max_length=10)
    is_default=models.BooleanField('是否默认地址',default=False)
    is_active=models.BooleanField('是否删除',default=True)

    username=models.ForeignKey(UserInfo,on_delete=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now_add=True)

    class Meta:
        db_table='user_address'



