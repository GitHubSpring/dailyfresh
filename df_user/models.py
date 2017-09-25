from django.db import models
from db.base_model import BaseModel  # 导入模型类基类
from utils.get_hash import get_hash  # 加密
from db.base_manager import BaseManager  # 导入模型管理器类基类


class PassportManager(BaseManager):
    """用户账户管理器类"""

    def add_one_passport(self, username, password, email):
        """添加一个用户注册信息"""
        obj = self.add_one_passport(username=username, password=get_hash(password), email=email)
        return obj

    def get_one_passport(self, username, password=None):
        """判断用户是否存在/判断用户名和密码是否正确"""
        if password:
            obj = self.get_one_object(username=username, password=get_hash(password))
        else:
            obj = self.get_one_object(username=username)
        return obj


class Passport(BaseModel):
    """用户账户类"""
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')  # sha1 加密 固长40
    email = models.EmailField(verbose_name='邮箱')  # 邮箱

    objects = PassportManager()  # 自定义管理器类对象

    class Meta:
        db_table = 's_user_account'


class AddressManager(BaseManager):
    """地址管理器类"""

    def get_one_address(self, passport_id):
        """获取账户默认收货地址"""
        self.get_one_object(passport_id=passport_id, is_default=True)

    def add_one_address(self, recipient_name, recipient_addr, recipient_phone, zip_code, passport_id):
        """给账户添加收货地址"""
        is_default = False
        if self.get_one_object(passport_id=passport_id) is None:
            # 当前没有收货地址, 第一次添加的收获地址默认为默认收货地址
            is_default = True
        self.add_one_object(recipient_name=recipient_name, recipient_addr=recipient_addr, recipient_phone=recipient_phone,
                            zip_code=zip_code, passport_id=passport_id, is_default=is_default)


class Address(BaseModel):
    """地址类"""

    passport = models.ForeignKey('Passport', verbose_name='所属账户')
    recipient_name = models.CharField(max_length=24, verbose_name='收件人')
    recipient_addr = models.CharField(max_length=128, verbose_name='收件地址')
    recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
    zip_code = models.CharField(max_length=6, verbose_name='邮政编码')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'
