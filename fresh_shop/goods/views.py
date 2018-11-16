from django.shortcuts import render

# Create your views here.
from cart.models import ShoppingCart
from goods.models import Goods, GoodsCategory
from utils.functions import login_required


# @login_required
def index(request):
    if request.method == 'GET':

        # {key1:[value1, value2], key2:[value3, value4]}
        goods = Goods.objects.all()
        categorys = GoodsCategory.CATEGORY_TYPE
        goods_dict = {}
        for category in categorys:
            goods_list = []
            count = 0
            for good in goods:
                # 判断商品分类和商品对象
                if count < 4:
                    if category[0] == good.category_id:
                        goods_list.append(good)
                        count += 1
            # {'新鲜水果':[], '羊肉':[]...}
            goods_dict[category[1]] = goods_list
        return render(request, 'index.html', {'goods_dict':goods_dict})


def detail(request, id):
    if request.method == 'GET':
        goods = Goods.objects.filter(id=id).first()
        return render(request, 'detail.html', {'goods':goods})


def list(request):
    if request.method == 'GET':
        return render(request, 'list.html')


def place_order(request):
    if request.method == 'GET':
        # 获取当前登录系统的user_id
        user_id = request.session['user_id']
        # 获取当前勾选的商品用于下单
        cart_goods = ShoppingCart.objects.filter(user_id=user_id)

        return render(request, 'place_order.html')

