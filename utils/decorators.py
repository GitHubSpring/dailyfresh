# 自定义装饰器
from django.shortcuts import redirect


def login_require(view_func):
    def inner(request, *view_args, **view_kwargs):
        if request.session.has_key('islogin'):
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect('/user/login/')
    return inner
