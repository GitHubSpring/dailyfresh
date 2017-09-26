from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseManager
from tinymce.models import HTMLField  # 导入富文本
from df_goods.enums import *  # 导入枚举


class GoodsLogicManager(BaseManager):
    """商品管理器逻辑类"""
    def get_goods_by_id(self, goods_id):
        """根据商品 id 查询商品信息, 包含商品详情图片"""
        goods = self.get_one_object(id=goods_id)
        # 查询商品的详情图片
        images = Image.objects.get_image_by_goods_id(goods_id=goods_id)
        # 给 goods 增加 images 属性
        goods.images = images

        return goods


class GoodsManager(BaseManager):
    """商品管理器类"""
    def get_goods_by_type(self, goods_type_id, limit=None, sort='default'):
        """
        根据商品类型id 查询商品信息,返回限定长度,并排序
        default: 默认排序, 按照主键的从大到小
        new: 新品, 按照商品创建时间排序
        price: 价格, 从小到大排序
        hot: 最热, 按照销量排序
        """
        order_by = '-pk'  # 默认
        if sort == 'price':
            order_by = 'price'
        elif sort == 'new':
            order_by = '-create_time'
        elif sort == 'hot':
            order_by = '-goods_sales'

        goods = self.get_object_list(filters={'goods_type_id': goods_type_id},
                                     order_by=(order_by, ))
        if limit:
            # 对查询结果集进行切片
            goods = goods[:limit]

        return goods

    def get_goods_by_id(self, goods_id):
        """根据商品 id 查询商品信息"""
        goods = self.get_one_object(id=goods_id)
        return goods


class Goods(BaseModel):
    """商品信息类"""
    goods_name = models.CharField(max_length=24, verbose_name='商品名称')
    goods_sub_title = models.CharField(max_length=128, verbose_name='商品副标题')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    goods_unite = models.CharField(max_length=10, verbose_name='商品单位')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='邮费')
    goods_image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    goods_info = HTMLField(verbose_name='商品描述')
    goods_stock = models.IntegerField(default=1, verbose_name='商品库存')
    goods_sales = models.SmallIntegerField(default=0, verbose_name='商品销量')
    """
    goods_status_choices = (
        (1, '上线'),
        (2, '下线')
    )
    """
    goods_status_choices = (
        (ONLINE, GOODS_STATUS[ONLINE]),
        (OFFLINE, GOODS_STATUS[OFFLINE])
    )
    goods_status = models.IntegerField(choices=goods_status_choices, default=ONLINE, verbose_name='商品状态')
    """
    goods_type_choices = (
        (1, '新鲜水果'),
        (2, '海鲜水产'),
        (3, '猪牛羊肉'),
        (4, '禽类蛋品'),
        (5, '新鲜蔬菜'),
        (6, '速冻食品')
    )
    """
    goods_type_choices = (
        (FRUITS, GOOD_TYPE[FRUITS]),
        (SEAFOOD, GOOD_TYPE[SEAFOOD]),
        (MEAT, GOOD_TYPE[MEAT]),
        (EGGS, GOOD_TYPE[EGGS]),
        (VEGETABLES, GOOD_TYPE[VEGETABLES]),
        (FROZEN, GOOD_TYPE[FROZEN])
    )

    goods_type_id = models.SmallIntegerField(choices=goods_type_choices, default=FRUITS, verbose_name='商品类型')

    objects = GoodsManager()
    objects_logic = GoodsLogicManager()  # 根据 id 可以查询商品信息和商品详情图片

    class Meta:
        db_table = 's_goods'


class ImageManager(BaseManager):
    """商品图片详情管理器类"""
    def get_image_by_goods_id(self, goods_id):
        """根据商品 id 查询详情图片"""
        images = self.get_object_list(filters={'goods_id': goods_id})
        if images.exists():
            # 取出第一张图片
            images = images[0]

        return images  # 可能是一个QuerySet(空列表), 也可能是一个Image对象(包含图片路径)


class Image(BaseModel):
    """商品详情图片类"""
    goods = models.ForeignKey('Goods', verbose_name='所属商品')
    img_url = models.ImageField(upload_to='goods', verbose_name='详情图片')

    objects = ImageManager()

    class Meta:
        db_table = 's_goods_image'
