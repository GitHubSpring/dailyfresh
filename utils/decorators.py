# 自定义装饰器
from django.shortcuts import redirect


def login_require(view_func):
    def inner(request, *args, **kwargs):
        if request.session['islogin']:
            view_func(request, *args, **kwargs)
        else:
            return redirect('/user/login/')
    return inner
