# 公共管理器类
from django.db import models
import copy


class BaseManager(models.Manager):
    """自定义模型管理器公共类, 都是通过传递关键字参数来增删改"""

    def get_all_vaild_fields(self):
        """获取所管理的类的所有有效属性列表"""
        attr_tuple = self.model._meta.get_fields()
        attr_list = []
        for attr in attr_tuple:
            # 将外键自动创建的 xxx_id 属性添加进来
            if isinstance(attr, models.ForeignKey):
                attr_list.append('%s_id' % attr.name)
            attr_list.append(attr.name)
        return attr_list

    def add_one_object(self, **kwargs):
        """添加一条记录, 去除无效属性"""
        # 1. 获取self.model 这个类所有有效属性
        all_fields = self.get_all_vaild_fields()
        # 2. 遍历字典,去掉无效属性
        kwargs_cp = copy.copy(kwargs)
        for key in kwargs_cp:
            if key not in all_fields:
                kwargs.pop(key)
        # 3. 根据筛选后的键值创建模型类
        obj = self.model(**kwargs)
        obj.save()

    def get_one_object(self, **kwargs):
        """查询一条记录"""
        try:
            obj = self.get(**kwargs)
        except self.model.DoesNotExist:
            obj = None

        return obj

    def get_object_list(self, filters={}, order_by=('-pk', )):
        """按照 filters 中的条件查询,并进行排序"""
        object_list = self.filter(**filters).order_by(*order_by)
        return object_list

