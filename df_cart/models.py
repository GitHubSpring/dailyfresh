from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseManager
from df_goods.models import Goods
from django.db.models import Sum

class CartManager(BaseManager):
    """购物车模型管理器类"""
    def get_one_cart_info(self, passport_id, goods_id):
        """从购物车中获取一条商品记录"""
        return self.get_one_object(passport_id=passport_id, goods_id=goods_id)

    def add_one_cart_info(self, passport_id, goods_id, goods_count):
        """添加一条记录到购物车"""
        # 判断是否超过库存
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        if goods_count > goods.goods_stock:
            # 超出, 添加失败
            return False
        # 暂未超, 判断用户购物车中是否已经存在该商品
        obj = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        if obj:
            # 存在,重新判断当前库存
            total_count = obj.goods_count + goods_count
            if total_count > goods.goods_stock:
                # 超出, 添加失败
                return False
            # 没超出, 修改商品数目
            obj.goods_count = total_count
            obj.save()
            return True
        else:
            # 不存在, 直接添加新记录
            self.add_one_object(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
            return True

    def get_total_cart_info(self, passport_id):
        """获取商品总数"""
        total_goods = self.filter(passport_id=passport_id).aggregate(Sum('goods_count'))
        # {'goods_count__sum': None/3}
        total_count = total_goods['goods_count__sum']
        if total_count is None:
            total_count = 0
        return total_count


class Cart(BaseModel):
    """购物车模型类"""
    passport = models.ForeignKey('df_user.Passport', verbose_name='所属用户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='所属商品')
    goods_count = models.IntegerField(default=1, verbose_name='商品数量')

    objects = CartManager()

    class Meta:
        db_table = 's_cart'
