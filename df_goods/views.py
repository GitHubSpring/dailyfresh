from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods
from django.http import JsonResponse


def home_list_page(request):
    """首页"""
    return render(request, 'df_goods/index.html')


def goods_detail(request, gid):
    """商品详情页"""
    return render(request, 'df_goods/detail.html')


# /goods/stock/数字/
@require_GET
def goods_stock(request):
    """商品库存"""
    return JsonResponse({'res': '库存量'})


# /goods/list/种类/页码/?sort=排序方式
@require_GET
def goods_list(request):
    """商品列表页"""
    return render(request, 'df_goods/list.html')
