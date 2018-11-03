from django.shortcuts import render

# Create your views here.
from back.models import Article


def gbook(request):
    if request.method == 'GET':
        return render(request, 'web/gbook.html')


def index(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        return render(request, 'web/index.html', {'articles':articles})


def info(request):
    if request.method == 'GET':
        return render(request, 'web/info.html')


def list(request):
    if request.method == 'GET':
        return render(request, 'web/list.html')

def infopic(request):
    if request.method == 'GET':
        return render(request, 'web/infopic.html')

def share(request):
    if request.method == 'GET':
        return render(request, 'web/share.html')

def about(request):
    if request.method == 'GET':
        return render(request, 'web/about.html')

def article(request, id):
    if request.method == 'GET':
        article = Article.objects.get(pk=id)
        return render(request, 'web/article.html', {'article':article})