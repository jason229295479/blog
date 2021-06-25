from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# 定义用户模型类 创建用户表

class User(AbstractUser):
    # 电话号码字段  unique唯一性字段
    mobile = models.CharField(max_length=11, unique=True, blank=False)
    # 头像字段 upload_to为保存到响应的子目录
    avatar = models.ImageField(upload_to='avatar/%Y%M%d/', blank=True)
    # 个人简介字段
    user_desc = models.TextField(max_length=500, blank=True)

    class Meta:
        db_table = 'blog_users'  # 修改表名
        verbose_name = '用户管理'  # admin后台显示
        verbose_name_plural = verbose_name  # admin后台显示

    def __str__(self):
        return self.mobile

    # 修改认证字段
# USERNAME_FIELD = 'mobile'

# 创建超级管理员的需要必须输入的字段
# REQUIRED_FIELDS = ['username', 'email']
