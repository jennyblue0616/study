from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from fresh_shop_back.settings import PAGE_NUMBER
from goods.forms import GoodsForm
from goods.models import GoodsCategory, Goods


# Create your views here.


def goods_category_list(request):
    if request.method == 'GET':
        # 返回商品分类对象
        categorys = GoodsCategory.objects.all()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_list.html', {'categorys':categorys, 'types':types})


def goods_category_detail(request, id):
        if request.method == 'GET':
            # 返回商品分类对象,和分类枚举信息
            category = GoodsCategory.objects.filter(pk=id).first()
            types = GoodsCategory.CATEGORY_TYPE
            return render(request, 'goods_category_detail.html', {'category':category, 'types':types})
        if request.method == 'POST':
            # 获取图片
            img = request.FILES.get('category_front_image')
            if img:
                category = GoodsCategory.objects.filter(pk=id).first()
                category.category_front_image = img
                category.save()
                return HttpResponseRedirect(reverse('goods:goods_category_list'))
            else:
                error = '图片必填'
                return render(request, 'goods_category_detail.html', {'error':error})


def goods_list(request):
    if request.method == 'GET':
        # TODO:查询所有的商品信息,并在goods_list页面解析
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            page = 1
        goods = Goods.objects.all()
        # 分页
        paginator = Paginator(goods, PAGE_NUMBER)
        gs = paginator.page(page)
        return render(request, 'goods_list.html', {'goods':goods, 'gs':gs, 'paginator':paginator})


def goods_add(request):
    if request.method == 'GET':
        # TODO:页面中刷新分类信息
        categorys = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_detail.html',{'categorys':categorys})
    if request.method == 'POST':
        # TODO:验证商品信息的完整性,数据的保存
        # category = GoodsCategory.objects.filter(category_type=request.POST.get('category')).first()
        #
        # goods = Goods()
        # goods.name = request.POST.get('name')
        # goods.goods_sn=request.POST.get('goods_sn')
        # goods.category=category
        # goods.goods_nums=request.POST.get('goods_nums')
        # goods.market_price=request.POST.get('market_price')
        # goods.shop_price=request.POST.get('shop_price')
        # goods.goods_front_image=request.FILES.get('goods_front_image')
        # goods.save()

        #1.使用表单验证
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            # 创建
            # Goods.objects.create(name=form.cleaned_data.get('name'),
            #                      category_id=form.cleaned_data.get('category'),
            #                      或者category=对象)
            # **data字典
            data = form.cleaned_data
            #category(对象)=form.cleaned_data.get('category')(id值=1)
            #(1)category_id
            #(2)category在form中重写方法,变成对象
            Goods.objects.create(**data)
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            #验证失败
            return render(request, 'goods_detail.html', {'errors':form.errors})

def goods_del(request, id):
    if request.method == 'POST':
        # 删除商品数据,使用ajax
        Goods.objects.filter(pk=id).delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def goods_edit(request, id):
    if request.method == 'GET':
        # 编辑商品对象
        goods = Goods.objects.filter(pk=id).first()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_detail.html', {'goods':goods, 'types':types})
    if request.method == 'POST':
        # 1.form表单校验
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            # 把图片从data中删掉
            # img表示更新商品时,选择了图片,则img为图片内容
            # 如果更新商品时没选图片,则img为None
            img = data.pop('goods_front_image')
            # 更新除了图片以外的其他字段信息
            Goods.objects.filter(pk=id).update(**data)
            # image = request.FILES.get('goods_front_image')
            # goods = Goods()
            # goods.goods_front_image=image
            # goods.save()
            if img:
                # 更新图片的信息
                goods = Goods.objects.filter(pk=id).first()
                goods.goods_front_image=img
                goods.save()
            return HttpResponseRedirect(reverse('goods:goods_list'))

        else:
            #修改验证失败
            goods = Goods.objects.filter(pk=id).first()
            types = GoodsCategory.CATEGORY_TYPE
            return render(request, 'goods_detail.html', {'errors':form.errors, 'types':types, 'goods':goods})


def goods_desc(request, id):
    if request.method == 'GET':
        # TODO:返回商品对象,并刷新编辑内容
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'goods_desc.html', {'goods':goods})
    if request.method == 'POST':
        # 获取编辑器的内容
        content = request.POST.get('content')
        # 获取修改商品对象
        goods = Goods.objects.filter(pk=id).first()
        # 保存商品的描述信息
        goods.goods_desc=content
        goods.save()
        return HttpResponseRedirect(reverse('goods:goods_list'))