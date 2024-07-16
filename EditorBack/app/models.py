from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=64)
    account = models.CharField(verbose_name="账号", max_length=64, unique=True)
    password = models.CharField(verbose_name="密码", max_length=128)
    accessToken = models.CharField(verbose_name="访问令牌", max_length=128, null=True)