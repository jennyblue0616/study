from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=10, required=True,
                               error_messages={'required':'账号必填'})
    password = forms.CharField(required=True,
                               error_messages={'required': '密码必填'})
    def clean(self):
        # 使用django自带的User模块进行验证
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        if not user:
            raise forms.ValidationError({'username':'该账户没有注册'})
        return self.cleaned_data
