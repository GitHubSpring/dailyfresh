from django.shortcuts import render
from django.views.decorators.http import require_GET
from df_goods.models import Goods
from df_user.models import BrowseHistory
from df_goods.enums import *  # 导入枚举
from django.core.paginator import Paginator  # 导入分页类


def home_list_page(request):
    """首页"""
    # 查询商品
    """
    key = ['fruits', 'seafood', 'meat', 'eggs', 'vegetables', 'frozen']
    context = {}
    for good_type in GOOD_TYPE:
        goods = Goods.objects.get_goods_by_type(goods_type_id=good_type, limit=4)
        goods_new = Goods.objects.get_goods_by_type(goods_type_id=good_type, limit=3, sort='new')
        t = (goods, goods_new)
        context[key[good_type-1]] = t

    print(context)
    """

    fruits = Goods.objects.get_goods_by_type(goods_type_id=FRUITS, limit=4)
    fruits_new = Goods.objects.get_goods_by_type(goods_type_id=FRUITS, limit=3, sort='new')

    seafood = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=4)
    seafood_new = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=3, sort='new')

    meat = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=4)
    meat_new = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=3, sort='new')

    eggs = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=4)
    eggs_new = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=3, sort='new')

    vegetables = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=4)
    vegetables_new = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=3, sort='new')

    frozen = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=4)
    frozen_new = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=3, sort='new')

    # 组织上下文数据
    context = {
        'fruits': fruits,
        'fruits_new': fruits_new,
        'seafood': seafood,
        'seafood_new': seafood_new,
        'meat': meat,
        'meat_new': meat_new,
        'eggs': eggs,
        'eggs_new': eggs_new,
        'vegetables': vegetables,
        'vegetables_new': vegetables_new,
        'frozen': frozen,
        'frozen_new': frozen_new,
    }

    return render(request, 'df_goods/index.html', context)


# /goods/gid/
def goods_detail(request, gid):
    """商品详情页, 根据商品 id 查询"""
    # 商品
    # goods = Goods.objects.get_goods_by_id(goods_id=gid)
    # 商品和商品详情图片
    goods = Goods.objects_logic.get_goods_by_id(goods_id=gid)
    # 新品推荐
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # 添加进浏览记录
    BrowseHistory.objects.add_one_history(passport_id=request.session.get('passport_id'), goods_id=gid)

    return render(request, 'df_goods/detail.html', {'goods': goods, 'goods_new': goods_new})


# /list/种类/页码/?sort=排序方式
@require_GET
def goods_list(request, goods_type_id, pindex):
    """商品列表页"""
    # 获取排序方式, 如果没有指定排序, 按默认方式(即按照-pk的方式)
    sort = request.GET.get('sort', 'default')
    # 根据goods_type_id获取商品信息
    goods = Goods.objects.get_goods_by_type(goods_type_id=goods_type_id, sort=sort)

    # 对查询结果进行分页
    paginator = Paginator(goods, 5)
    pindex = int(pindex)
    goods = paginator.page(pindex)  # 获取第 pindex 页的内容
    nums_pages = paginator.num_pages  # 获取分页后的总页数
    if nums_pages < 5:
        # 不足5页,页码全显示
        pages = range(1, nums_pages + 1)
    elif pindex <= 3:
        # 当前是前3页, 显示前5页
        pages = range(1, 6)
    elif nums_pages - pindex < 3:  # 6 7 8 9 10
        # 当前是后3页, 显示后5页
        pages = range(nums_pages - 4, nums_pages + 1)
    else:
        # 其他情况, 显示当前页, 当前页的前两页和后两页
        pages = range(pindex - 2, pindex + 3)

    # 查询新品推荐
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods_type_id, limit=2, sort='new')

    # 定义上下文
    context = {
        'goods': goods,
        'goods_new': goods_new,
        'pages': pages,  # 页码范围
        'type_title': GOOD_TYPE[int(goods_type_id)],
        'type_id': goods_type_id,
        'sort': sort
    }
    return render(request, 'df_goods/list.html', context)
