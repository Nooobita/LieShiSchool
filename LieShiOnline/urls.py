# coding: utf-8
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.views.generic import TemplateView
from users.views import user_login
from users.views import LoginView, RegisterView, ActiveUserView, ForgetView, ResetView,\
    ModifyPwdView, LogoutView, IndexView
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
   # url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'), # 配置静态首页
    # url(r'^login/$', user_login, name="login") # 函数方式定义视图
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='active_code'),
    url(r'^forget/$', ForgetView.as_view(), name='forget'),
    url(r'^reset/(?P<active_code>.*)$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^$', IndexView.as_view(), name='index'),

    # 课程机构页面
    url(r'^org/', include("organization.urls", namespace='org')),

    # 配置上传的文件的访问处理
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 配置静态资源处理
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 公开课页面
    url(r'^courses/', include("courses.urls", namespace='courses')),

    # 用户中心
    url(r'users/', include("users.urls", namespace='users')),

    #Ueditor路径配置
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]

# 404错误页面配置
handler404 = 'users.views.page_not_found'
# 403错误页面配置
handler403 = 'users.views.page_error'
# 500错误页面配置
handler500 = 'users.views.page_forbidden'
