from django.conf.urls import url
from df_user import views

urlpatterns = [
    url(r'^register/$', views.register),  # 注册页面(get)/注册处理(post)
    url(r'^check_user_exist/$', views.check_user_exist),  # 验证用户名是否已经存在

    url(r'^login/$', views.login),  # 登录界面(get)/登录处理(post)
    url(r'^logout/$', views.logout),  # 退出登录
    url(r'^', views.user),  # 用户中心-用户信息页
]
