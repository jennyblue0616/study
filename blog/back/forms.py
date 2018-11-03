from django import forms
from django.contrib.auth.models import User


class Register(forms.Form):
    username = forms.CharField(required=True,
                               max_length=10,
                               min_length=2)
    password = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError({'username':'已经注册过'})
        pw = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password2')
        if pw != pw2:
            raise forms.ValidationError({'password':'密码不对'})
        return self.cleaned_data

class Login(forms.Form):
    username = forms.CharField(max_length=10, min_length=2, required=True)
    password = forms.CharField(required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username': '该账号没有注册,请去注册'})
        return self.cleaned_data
