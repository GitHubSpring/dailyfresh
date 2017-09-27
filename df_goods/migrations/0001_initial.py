# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('goods_name', models.CharField(verbose_name='商品名称', max_length=24)),
                ('goods_sub_title', models.CharField(verbose_name='商品副标题', max_length=128)),
                ('goods_price', models.DecimalField(verbose_name='商品价格', max_digits=10, decimal_places=2)),
                ('goods_unite', models.CharField(verbose_name='商品单位', max_length=10)),
                ('transit_price', models.DecimalField(verbose_name='邮费', max_digits=10, decimal_places=2)),
                ('goods_image', models.ImageField(verbose_name='商品图片', upload_to='goods')),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品描述')),
                ('goods_stock', models.IntegerField(verbose_name='商品库存', default=1)),
                ('goods_sales', models.SmallIntegerField(verbose_name='商品销量', default=0)),
                ('goods_status', models.IntegerField(verbose_name='商品状态', default=1, choices=[(1, '上线商品'), (0, '下线商品')])),
                ('goods_type_id', models.SmallIntegerField(verbose_name='商品类型', default=1, choices=[(1, '新鲜水果'), (2, '海鲜水产'), (3, '猪牛羊肉'), (4, '禽类蛋品'), (5, '新鲜蔬菜'), (6, '速冻食品')])),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('img_url', models.ImageField(verbose_name='详情图片', upload_to='goods')),
                ('goods', models.ForeignKey(verbose_name='所属商品', to='df_goods.Goods')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
