from django.conf.urls import url
from df_cart import views

urlpatterns = [
    url(r'^add/$', views.cart_add),  # 添加到购物车
    url(r'^count/$', views.cart_count),  # 获取购物车中商品总数
    url(r'^$', views.cart_show),  # 购物车页
    url(r'^update/$', views.cart_update),  # 更新购物车商品数量
]
