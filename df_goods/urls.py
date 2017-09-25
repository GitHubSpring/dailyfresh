from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r'^goods/$', views.home_list_page),  # 首页
    url(r'^goods/(\d+)/$', views.goods_detail),  # 商品详情页
    url(r'^goods/stock/(\d+)/', views.goods_stock),  # 商品库存

    url(r'^goods/list/$', views.goods_list),  # 商品列表页 /goods/list/种类/页码/?sort=排序方式
]
