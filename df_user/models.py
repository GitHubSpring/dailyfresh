from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash  # 加密


class PassportManager(models.Manager):
    """用户账户管理器类"""

    def add_one_passport(self, username, password, email):
        """添加一个用户注册信息"""
        obj = self.model(username=username, password=get_hash(password), email=email)
        obj.save()
        return obj

    def get_one_passport(self, username, password=None):
        """判断用户是否存在/判断用户名和密码是否正确"""
        try:
            if password:
                obj = self.get(username=username, password=get_hash(password))
            else:
                obj = self.get(username=username)
        except self.model.DoesNotExist:
            obj = None
        return obj


class Passport(BaseModel):
    """用户账户类"""
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')  # sha1 加密 固长40
    email = models.EmailField(verbose_name='邮箱')  # 邮箱

    objects = PassportManager()  # 自定义管理器类对象

    class Meta:
        db_table = 's_user_account'
