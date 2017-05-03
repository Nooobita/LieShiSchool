# coding: utf-8
__author__ = 'nobita'
__date__ = '1/22/2017 15:28'

from django import forms
from operation.models import UserAsk
import re


class AddUserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            return forms.ValidationError(u"手机号码非法", code="mobile_invail")