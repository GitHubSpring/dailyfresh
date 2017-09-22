from django.conf.urls import url
from df_user import views

urlpatterns = [
    url(r'^register/$', views.register),  # 注册页面
    url(r'^register_handler/$', views.register_handler),  # 注册处理
    url(r'^check_user_exist/(?P<username>\w+)/$', views.check_user_exist),  # 验证用户名是否已经存在

    url(r'^login/$', views.login),  # 登录界面
    url(r'^login_check/$', views.login_check),  # 登录处理

    url(r'^index/$', views.index),  # 首页
]
