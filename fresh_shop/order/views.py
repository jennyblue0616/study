import random

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import ShoppingCart
from fresh_shop.settings import PAGE_NUMBER
from order.models import OrderGoods, OrderInfo
from user.models import UserAddress
from utils.functions import get_order_sn

def order(request):
    if request.method == 'POST':
        """
        接收ajax请求，创建订单
        """
        # 1. 选择购物车中is_select为True的商品
        # 2. 创建订单
        # 3. 创建订单和商品之间的关联关系表，order_goods表
        # 4. 删除购物车中已下单的商品
        # 1.从购物车中取出当前登录系统用户和select为1的商品信息
        user_id = request.session.get('user_id')
        # 获取收货人的地址id
        address_id = request.POST.get('address_id')
        user_address = UserAddress.objects.filter(id=address_id).first()
        carts = ShoppingCart.objects.filter(user_id=user_id,
                                    is_select=1).all()
        # 订单货号
        order_sn = get_order_sn()
        # 计算总金额
        order_mount = 0
        for cart in carts:
            order_mount += int(cart.nums) * int(cart.goods.shop_price)

        # 2.创建订单
        order = OrderInfo.objects.create(user_id=user_id,
                                         order_sn=order_sn,
                                         order_mount=order_mount,
                                         address=user_address.address,
                                         signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile)
        # 3.创建订单详情信息
        for cart in carts:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums)
        # 4.删除购物车中已经下单的信息
        carts.delete()
        if request.session.get('goods'):
            request.session.pop('goods')

        return JsonResponse({'code':200, 'msg':'请求成功'})


def user_order(request):

    if request.method == 'GET':
        user = request.user
        # 获取分页
        try:
            # 如果page参数不能转化为int类型，则异常，默认page为1
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        # 获取当前用户所有的订单信息
        order_info = OrderInfo.objects.filter(user=user)
        paginator = Paginator(order_info, PAGE_NUMBER)
        order_info = paginator.page(page)
        order_status = OrderInfo.ORDER_STATUS
        return render(request, 'user_center_order.html', {'order_info': order_info, 'order_status': order_status})


def user_order_site(request):

    if request.method == 'GET':
        user = request.user
        user_addresses = UserAddress.objects.filter(user=user).order_by('-id')

        return render(request, 'user_center_site.html', {'user_addresses': user_addresses})





