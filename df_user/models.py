from django.db import models
from db.base_model import BaseModel
# from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher
from hashlib import sha1
from django.db.models import Q


class PassportManager(models.Manager):
    """用户账户管理器类"""
    def add_one_passport(self, username, password, email):
        """添加一个用户注册信息"""
        obj = self.model(username=username, password=password, email=email)
        obj.save()
        return obj

    def is_exist_by_username(self, username):
        """通过用户名查看用户是否已注册"""
        obj = self.model.objects.filter(username=username)
        if len(obj) == 0:
            return 0  # 不存在

        return 1  # 存在

    def is_correct(self, username, password):
        """判断用户名和密码是否正确"""
        obj = self.model.objects.filter(Q(username=username) & Q(password=password))
        if len(obj) == 0:
            return 0  # 错误

        return 1  # 正确


class Passport(BaseModel):
    """用户账户类"""
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')  # sha1 加密 固长40
    email = models.EmailField(verbose_name='邮箱')  # 邮箱

    objects = PassportManager()  # 自定义管理器类对象

    class Meta:
        db_table = 's_user_account'

