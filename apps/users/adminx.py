# coding: utf-8
__author__ = 'nobita'
__date__ = '1/19/2017 16:48'

import xadmin

from .models import EmailVerifyRecord, Banner, UserProfile
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "猎识后台管理系统"
    site_footer = "猎识在线网"
    menu_style = "accordion"


class UserAdmin(object):
    list_display = ['username', 'email', 'is_staff', 'is_active', 'gender', 'address']
    search_fields = ['username', 'email', 'is_staff', 'is_active', 'gender', 'address']
    list_filter = ['username', 'email', 'is_staff', 'is_active', 'gender', 'address']
    model_icon = 'fa fa-user-circle-o'
    list_per_page = 10
    relfield_style = 'fk-ajax'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-envelope-open-o'
    exclude = ('send_time', )
    list_per_page = 10


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    model_icon = 'fa fa-picture-o'
    exclude = ('add_time', )
    list_per_page = 10


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(UserProfile, UserAdmin)
