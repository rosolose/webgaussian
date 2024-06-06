from django.db import models
from django.utils import timezone

# Create your models here.
"""用户表"""
class User(models.Model):  
    id = models.BigAutoField(primary_key=True)  # 自增的BigIntegerField主键，Django 3.2+ 使用 BigAutoField  
    username = models.CharField(max_length=32, unique=True)  # 学号作为用户名，且唯一  
    pwd = models.CharField(max_length=64)  # 密码（在生产环境中，通常会对密码进行哈希处理）  
    nickname = models.CharField(max_length=10)  # 昵称，不超过10字符  
    avatar = models.CharField(max_length=255, blank=True, null=True)  # 头像路径，可为空  
    signature = models.CharField(max_length=20, blank=True, null=True)  # 个性签名，不超过20字符，可为空  
    state = models.IntegerField(choices=((1, '正常'), (0, '封号')), default=1)  # 账号状态，1正常 0封号  
    create_time = models.DateTimeField(default=timezone.now)  # 注册时间，默认为当前时间  
    update_time = models.DateTimeField(auto_now=True)  # 修改时间，每次保存对象时自动更新为当前时间  
  
    def __str__(self):  
        return self.username  