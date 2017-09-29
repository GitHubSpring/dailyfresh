from django.shortcuts import render
from utils.decorators import login_require  # 导入登录装饰器
from django.http import JsonResponse
from df_cart.models import Cart


# /cart/add/
@login_require
def cart_add(request):
    """添加商品到购物车"""
    goods_id = request.GET.get('goods_id')
    goods_count = int(request.GET.get('goods_count'))
    passport_id = request.session.get('passport_id')
    if Cart.objects.add_one_cart_info(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count):
        # 添加成功
        return JsonResponse({'res': 1})
    # 添加失败
    return JsonResponse({'res': 0})


def cart_count(request):
    """获取购物车中商品总数"""
    total_count = Cart.objects.get_total_cart_info(passport_id=request.session.get('passport_id'))
    return JsonResponse({'res': total_count})


@login_require
def cart_show(request):
    """购物车页"""
    return render(request, 'df_cart/cart.html')
