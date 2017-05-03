# coding: utf-8
__author__ = 'nobita'
__date__ = '1/20/2017 16:50'

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile
import re


class LoginForms(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForms(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u"验证码不正确!"})


class ForgetForms(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u"验证码不正确!"})


class ModifyForms(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


# 修改用户数据
class ModifyUserForms(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            return forms.ValidationError(u"手机号码非法", code="mobile_invail")


# 用户修改头像
class ImageUploadForms(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image', ]
