from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from back.forms import Register, Login
from back.models import Article, Category


def register(request):
    if request.method == 'GET':
        return render(request, 'back/register.html')
    if request.method == 'POST':
        data = request.POST
        form = Register(data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username,password=password)
            return HttpResponseRedirect(reverse('back:login'))
        else:
            errors = form.errors
            return render(request, 'back/register.html',{'errors':errors} )


def login(request):
    if request.method == 'GET':
        return render(request, 'back/login.html')
    if request.method == 'POST':
        data = request.POST
        form = Login(data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('back:index'))
            else:
                return render(request,'back/login.html',{'msg':'密码错误'})
        else:
            return render(request, 'back/login.html', {'errors':form.errors})


@login_required
def index(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        return render(request, 'back/index.html', {'articles':articles})


@login_required
def logout(request):
    if request.method == 'GET':
        return render(request, 'back/login.html')


def article(request):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        articles = Article.objects.all()
        paginator = Paginator(articles, 5)
        arts = paginator.page(page)
        return render(request, 'back/article.html', {'articles':articles, 'arts':arts})


def category(request):
    if request.method == 'GET':
        categorys = Category.objects.all()
        return render(request, 'back/category.html', {'categorys':categorys})
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        Category.objects.create(name=name, desc=desc)
        return HttpResponseRedirect(reverse('back:category'))


def add_article(request):
    if request.method == 'GET':

        return render(request, 'back/add-article.html')
    if request.method == 'POST':
        img = request.FILES.get('img')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        content = request.POST.get('content')
        Article.objects.create(img=img,title=title,desc=desc,content=content)

        c2 = Category.objects.filter(id=2).first()
        a2 = Article.objects.filter(title__contains='django').first()
        a2.category_set.add(c2)


        return HttpResponseRedirect(reverse('back:article'))


def update_article(request, id):

    article = Article.objects.get(pk=id)
    if request.method == 'POST':
        img = request.FILES.get('img')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        content = request.POST.get('content')
        Article.objects.filter(id=id).update(title=title,desc=desc,content=content)
        return HttpResponseRedirect(reverse('back:article'))
    else:
        return render(request, 'back/update-article.html', {'article': article})

def delete_article(request, id):
    if request.method == 'GET':
        article = Article.objects.get(id=id)
        article.delete()
        return HttpResponseRedirect(reverse('back:article'))