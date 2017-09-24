from django.shortcuts import render, redirect
from df_user.models import Passport
from django.http import JsonResponse

from df_user.tasks import send_register_success_email  # 使用 celery 中的 task 任务函数
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from utils.decorators import login_require  # 登录装饰器

# /user/register
@require_http_methods(['GET', 'POST'])
def register(request):
    """注册页/注册处理"""
    if request.method == 'GET':
        # get 方式为显示注册页
        return render(request, 'df_user/register.html')
    else:
        # post 方式则注册
        # 1. 拿到数据
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        # 2. 将数据添加到数据库
        Passport.objects.add_one_passport(username=username, password=pwd, email=email)
        # 3. 发送邮件
        send_register_success_email.delay(username, pwd, email)
        # 4. 跳转到登录界面
        return redirect('/user/login/')


@require_GET
def check_user_exist(request):
    """验证用户名是否已经存在"""
    obj = Passport.objects.is_exist_by_username(request.GET.get('username'))
    if obj:
        return JsonResponse({'res': 1})
    return JsonResponse({'res': 0})


@require_http_methods(['POST', 'GET'])
def login(request):
    """登录界面/登录处理"""
    if request.method == 'GET':
        # 登录界面
        return render(request, 'df_user/login.html')
    # 登录处理
    # 1. 获取信息
    username = request.POST.get('username')
    pwd = request.POST.get('password')

    # 2. 查询数据库是否存在并正确
    obj = Passport.objects.is_correct(username=username, password=pwd)
    print(username, pwd,obj)
    if obj:
        # 存在 判断是否记住用户名
        if request.POST.get('remember'):
            jres = JsonResponse({'res': 1})
            jres.set_cookie('username', username)

        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = obj.id
        return jres

    # 用户名或密码错误
    return JsonResponse({'res': 0})


def logout(request):
    """登出"""
    request.session.flush()
    # 重定向到首页
    return redirect('/')


@login_require
def user(request):
    """用户中心-用户信息页"""
    return render(request, 'df_user/user_center_info.html')


def order(request):
    """用户中心-订单页"""
    return render(request, 'df_user/user_center_order.html')


def site(request):
    """用户中心-地址页"""
    return render(request, 'df_user/user_center_site.html')

