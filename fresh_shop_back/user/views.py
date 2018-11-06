from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from user.forms import UserLoginForm


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        data = request.POST
        form = UserLoginForm(data)
        if form.is_valid():
            # 表单验证用户名和密码
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            user = auth.authenticate(username=username, password=password)
            if user:
                # 实现登录,request.user等于登录系统的用户
                auth.login(request, user)
                return HttpResponseRedirect(reverse('user:index'))
            else:
                return render(request, 'login.html')
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors':errors})


@login_required
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

@login_required
def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect(reverse('user:login'))

