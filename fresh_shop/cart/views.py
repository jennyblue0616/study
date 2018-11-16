from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import ShoppingCart
from goods.models import Goods
from user.models import User, UserAddress


def add_cart(request):
    if request.method == 'POST':
        # 加入到购物车,需判断用户是否登录
        # 如果登录,加入到购物车的数据,其实就是加入到数据库表中(优化成直接加到session中)
        # 因为最后都要把session中的数据同步到数据库中,通过中间件

        # 如果登录,加入到购物车的数据,存储到session中(优化后的)
        # 如果没有登录,则加入到session中
        # session中存储数据:商品id,商品数量,商品选择状态

        # 如果登录,则把session中的数据同步到数据库中(中间件同步数据)

        # 1.获取商品id和数量
        goods_id = int(request.POST.get('goods_id'))
        goods_num = int(request.POST.get('goods_num'))
        # 2.组装存到session中的数据格式,1是选中的状态
        goods_list = [goods_id, goods_num, 1]
        # {'goods':[[1,2,1],[2,5,1]...]}
        if request.session.get('goods'):
            # 判断session有没有商品数据
            # 说明session中存储了加入到购物车的商品信息
            # 判断当前加入到购物车中的数据,是否已经存在于session中
            # 如果存在,则修改session中该商品的数量
            # 如果不存在,则新增
            flag = 0
            session_goods = request.session['goods']
            for goods in session_goods:
                # 判断如果加入到购物车中数据,已经存在于session中,则修改数量
                if goods[0] == goods_id:
                    goods[1] = int(goods[1]) + int(goods_num)
                    flag = 1
            # 如果不存在,则添加
            if not flag:
                session_goods.append(goods_list)
            request.session['goods'] = session_goods
            goods_count = len(session_goods)
        else:
            # session中一个商品都没有,就添加商品
            data = []
            data.append(goods_list)
            request.session['goods'] = data
            goods_count = 1
        return JsonResponse({'code': 200, 'msg': '请求成功', 'goods_count':goods_count})


def cart(request):
    if request.method == 'GET':
        # 如果没有登录,则从session中取商品的信息
        # 如果登录,还是从session中取数据(保证数据库中的商品和session中商品一致)
        session_goods = request.session.get('goods')
        # 获取session中所有的商品id值
        if session_goods:
            goods_all = []
            for goods in session_goods:
                cart_goods = Goods.objects.filter(pk=goods[0]).first()
                goods_number = goods[1]
                total_price = goods[1] * cart_goods.shop_price
                goods_all.append([cart_goods, goods_number, total_price])
            # 获取商品对象
            # 前台需要商品信息,商品的个数,商品的总价
            # 后台返回结构[[goods objects, number, total_price],[goods objects, number, total_price]]
        else:
            goods_all = ''
        return render(request, 'cart.html', {'goods_all':goods_all})


def place_order(request):
    if request.method == 'GET':
        # 获取当前登录系统的user_id
        user_id = request.session.get('user_id')
        # 获取当前勾选的商品用于下单
        carts = ShoppingCart.objects.filter(user_id=user_id,
                                    is_select=1).all()
        for cart in carts:
            # 给每一个购物车商品对象添加一个total_price属性
            cart.total_price = int(cart.nums) * int(cart.goods.shop_price)
        # 获取订单地址
        addresses = UserAddress.objects.filter(user_id=user_id)
        return render(request, 'place_order.html', {'carts':carts, 'addresses':addresses})


def cart_count(request):
    if request.method == 'GET':
        # 判断购物车中商品的个数
        user_id = request.session.get('user_id')
        if user_id:
            # 如果用户登录.则返回购物车表中商品的个数
            count = ShoppingCart.objects.filter(user_id=user_id).count()
        else:
            # 如果没有登录,则返回session中商品的个数
            session_goods = request.session.get('goods')
            count = len(session_goods)
        return JsonResponse({'code':200, 'msg':'请求成功', 'count':count})


def f_price(request):
    """
    返回购物车或session中商品的价格和总价
    {goods_price:[[id1, price1], [id2, price2]], all_price: all_price}
    """
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            # 获取当前登录系统的用户的购物车中的数据
            carts = ShoppingCart.objects.filter(user_id=user_id)
            cart_data = {}
            cart_data['goods_price'] = [(cart.goods_id,
                                         cart.nums * cart.goods.shop_price)
                                        for cart in carts]
            all_price = 0
            # 总的价格
            for cart in carts:
                # if cart.is_select:
                all_price += cart.nums * cart.goods.shop_price
            cart_data['all_price'] = all_price
        else:
            # 拿到session中所有商品信息,[id, num, is_select]
            session_goods = request.session.get('goods')
            # 返回数据结构, {'goods_price':[[id1, price1], [id2, price2]]}
            cart_data = {}
            data_all = []
            # 计算总价
            all_price = 0
            for goods in session_goods:
                data = []
                data.append(goods[0])
                g = Goods.objects.filter(pk=goods[0])
                data.append(int(goods[1]) * g.shop_price)
                # 生成的data为:[id1, price1]
                data_all.append(data)
                # 判断如果商品勾选了,才计算总价格
                # if goods[2]:
            all_price += int(goods[1]) * g.shop_price
            cart_data['goods_price'] = data_all
            cart_data['all_price'] = all_price
        return JsonResponse({'code':200, 'cart_data':cart_data})

# 先进行商品个数的修改,和选择状态的修改,然后登陆的保存在表中,没登录保存在session
# ajax成功时调用计算价格f_price()函数
def change_goods_num(request):
    if request.method == 'POST':
        #修改购物车中商品的个数
        #1.先判断用户登录与否,如果没登录,修改session中商品的个数
        #2.用户登录,需要判断当前修改的商品是否存在于session中,如果存在,则修改session.如果不存在,则修改购物车表
        # 获取修改的商品id,个数,选择状态
        goods_id = request.POST.get('goods_id')
        goods_num = int(request.POST.get('goods_num'))
        is_select = int(request.POST.get('is_select'))
        user_id = request.session.get('user_id')
        #先判断要修改的商品是否存在于session中,如果存在则修改session中商品的个数和选择状态
        session_goods = request.session.get('goods')
        # goods的结构为:[id1, num1, is_select]
        if session_goods:
            for goods in session_goods:
                if int(goods_id) == int(goods[0]):
                    #修改session中商品信息
                    goods[1] = goods_num
                    goods[2] = is_select
            request.session['goods']=session_goods
        #如果用户登录了,则需要在修改购物车中数据,因为session中的商品有可能并不在购物车表中
        if user_id:
            #修改购物车中商品个数
            ShoppingCart.objects.filter(user_id=user_id, goods_id=goods_id).update(nums=goods_num,is_select=is_select)

        return JsonResponse({'code':200, 'msg':'请求成功'})


def delete_goods(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        goods = request.POST.get('goods')
        for session_goods in goods:
            if session_goods[0] == goods_id:
                goods.delete(session_goods)
        user_id = request.session.get('user_id')

        if user_id:
            ShoppingCart.objects.filter(user_id=user_id, goods_id=goods_id).delete()
        return JsonResponse({'code':200, 'msg':'删除成功'})