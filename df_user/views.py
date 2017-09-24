from django.shortcuts import render, redirect
from df_user.models import Passport, Address
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
    obj = Passport.objects.get_one_passport(username=request.GET.get('username'))
    if obj:
        return JsonResponse({'res': 1})
    return JsonResponse({'res': 0})


@require_http_methods(['POST', 'GET'])
def login(request):
    """登录界面/登录处理"""
    if request.method == 'GET':
        # 登录界面
        username = ''
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')

        return render(request, 'df_user/login.html', {'username': username})
    # 登录处理
    # 1. 获取信息
    username = request.POST.get('username')
    pwd = request.POST.get('password')

    # 2. 查询数据库是否存在并正确
    obj = Passport.objects.get_one_passport(username=username, password=pwd)
    if obj:
        # 判断是否有记录上一次访问的地址
        if request.session.has_key('pre_url_path'):
            next_path = request.session['pre_url_path']
        else:
            next_path = '/'  # 默认跳转到首页
        # 将结果和地址返回
        jres = JsonResponse({'res': 1, 'next_path': next_path})
        # 存在 判断是否记住用户名
        if request.POST.get('remember') == 'true':
            jres.set_cookie('username', username, max_age=14 * 86400)

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
    # 获取用户的默认收货信息
    obj = Address.objects.get_one_address(request.session['passport_id'])
    return render(request, 'df_user/user_center_info.html', {'page': 'info', 'address': obj})


@login_require
def order(request):
    """用户中心-订单页"""
    return render(request, 'df_user/user_center_order.html', {'page': 'order'})


@login_require
def address(request):
    """用户中心-地址页"""
    if request.method == 'GET':
        # 查看是否有默认地址
        obj = Address.objects.get_one_address(request.session['passport_id'])
        return render(request, 'df_user/user_center_site.html', {'page': 'address', 'address': obj})

    # post 添加收货地址
    recipient_name = request.POST.get('recipient_name')
    recipient_addr = request.POST.get('recipient_addr')
    zip_code = request.POST.get('zip_code')
    recipient_phone = request.POST.get('recipient_phone')
    Address.objects.add_one_address(recipient_name=recipient_name, recipient_addr=recipient_addr,
                                    recipient_phone=recipient_phone,
                                    passport_id=request.session['passport_id'],
                                    zip_code=zip_code)
    # 刷新, 即 get 访问地址页
    return redirect('/user/address/')
