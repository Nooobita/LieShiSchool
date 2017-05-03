# coding: utf-8
__author__ = 'nobita'
__date__ = '1/23/2017 22:05'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# 通过装饰器,验证用户登录
class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
