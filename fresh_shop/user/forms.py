from django import forms

from user.models import User


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(required=True, min_length=5, max_length=20)
    pwd = forms.CharField(required=True, min_length=8, max_length=20)
    cpwd = forms.CharField(required=True, min_length=8, max_length=20)
    email = forms.CharField(required=True)

    def clean(self):
        # 先判断用户是否注册
        user = User.objects.filter(username=self.cleaned_data.get('user_name')).first()
        if user:
            raise forms.ValidationError({'user_name':'该账户已经注册'})
        if self.cleaned_data.get('pwd') != self.cleaned_data.get('cpwd'):
            raise forms.ValidationError({'pwd':'密码不正确'})
        return self.cleaned_data

class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    pwd = forms.CharField(required=True)
    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        if not user:
            raise forms.ValidationError({'username':'该账户没有注册,请去注册'})

        return self.cleaned_data


class UserAddressForm(forms.Form):
    # 用户地址保存的表单验证
    signer_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    signer_postcode = forms.CharField(required=True)
    signer_mobile = forms.CharField(required=True, max_length=11)
