from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User
import re

class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        #TODO:某些页面需要登录才能访问,某些不需要登录就可以访问
        #TODO:需要登录的页面,当用户没有登录时,该如何处理?

        #给request.user赋值,赋的值为当前登录系统的用户对象
        # 如果登录,就赋值给request.user,页面最上方会显示用户名
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
            # 可以访问所有的页面
            return None

        # 如果没有登录(user_id),则分两种页面,一种是必须登录能访问,一种是不用登录也能访问,然后就是判断
        #思路: 首页,详情页面,登录,注册,访问media,static不管登录与否都可以查看
        #      下单,结算,订单页面,个人中心只能登录才能查看,没有登录跳转到登录页面
        # 第一种:不用登录也能访问
        not_need_path = ['/user/login/', '/user/register/',
                         '/goods/index/', '/goods/detail/(.*)/',
                         '/media/(.*)', '/static/(.*)','/cart/add_cart/',
                         '/cart/cart/', '/cart/cart_count/','/cart/f_price/',
                         '/cart/change_goods_num/']
        path = request.path
        for not_path in not_need_path:
            #匹配当前路径是否为不需要登录验证的路径
            if re.match(not_path, path):
                return None
        #当前的请求url不在not_need_path中,则表示当前url需要登录才能访问
        # 第二种:登录才能访问,没登录就跳转登录页面

        # 如果访问首页,则直接访问首页方法
        if path == '/':
            return None
        return HttpResponseRedirect(reverse('user:login'))


class SessionUpdate(MiddlewareMixin):

    def process_request(self, request):
        # session 中商品数据和购物车表中数据的同步操作
        # session数据结构:[[id, num, is_select],[],[]]
        session_goods = request.session.get('goods')
        user_id = request.session.get('user_id')
        if user_id:
            # 用户登陆后才做同步
            if session_goods:
            # 思路:时刻保持session中数据和数据库中数据同步
            # 如果session中商品已经存在于数据库表中,则更新
            # 如果session中商品不存在于数据库表中,则添加
            # 如果session中商品少于数据库表中商品,则更新session

                # 将session中数据添加到数据库
                for goods in session_goods:
                    # goods的结构[id, num, is_select]
                    cart = ShoppingCart.objects.filter(user_id=user_id,
                                                goods_id=goods[0]).first()
                    if cart:
                        # 数据库中能查询到该商品信息,则修改
                        cart.nums = goods[1]
                        cart.is_select = goods[2]
                        cart.save()
                    else:
                        # 数据库中查询不到该商品信息,则添加
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=goods[0],
                                                    nums=goods[1],
                                                    is_select=goods[2])

            # 将数据库数据同步到session
            carts = ShoppingCart.objects.filter(user_id=user_id).all()
            # session数据结构:[[id, num, is_select],[],[]]
            session_new_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in carts]
            # 重新给request.session赋值
            request.session['goods'] = session_new_goods
        return None


