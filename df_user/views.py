from django.shortcuts import render, redirect
from df_user.models import Passport
from django.http import JsonResponse
from hashlib import sha1


# /user/register
def register(request):
    """注册页"""
    return render(request, 'df_user/register.html')


def register_handler(request):
    """注册处理"""
    # 1. 拿到数据
    username = request.POST.get('user_name')
    pwd = sha1(request.POST.get('pwd').encode('utf-8')).hexdigest()
    email = request.POST.get('email')
    # 2. 将数据添加到数据库

    Passport.objects.add_one_passport(username=username, password=pwd, email=email)
    # 3. 跳转到登录界面
    return redirect('/user/login/')


def check_user_exist(request, username):
    """验证用户名是否已经存在"""
    res = Passport.objects.is_exist_by_username(username)
    return JsonResponse({'res': res})


def login(request):
    """登录界面"""
    return render(request, 'df_user/login.html')


def login_check(request):
    """登录处理"""
    # 1. 获取信息
    username = request.POST.get('username')
    pwd = sha1(request.POST.get('pwd').encode('utf-8')).hexdigest()
    # 2. 查询数据库是否存在并正确
    res = Passport.objects.is_correct(username=username, password=pwd)
    if res == 1:
        return redirect('/user/index/')
    # 用户名或密码错误
    return redirect('/user/login/')


def index(request):
    """首页"""
    return render(request, 'df_user/index.html')
