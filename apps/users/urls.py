# coding: utf-8
__author__ = 'nobita'
__date__ = '1/24/2017 14:47'

from django.conf.urls import url
from .views import UserInfoView, UserCourseView, UserCollectOrgView,\
    UserCollectTeacherView, UserCollectCourseView, UserMessageView,\
    ImageUploadView, UserReSetPwdView, SendCodeToEmailView, VerifyCodeView

urlpatterns = [

    # 用户中心首页
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    # 用户课程页面
    url(r'^course/$', UserCourseView.as_view(), name='user_course'),

    # 用户收藏--机构页面
    url(r'^collect/org/$', UserCollectOrgView.as_view(), name='user_collect_org'),

    # 用户收藏--讲师页面
    url(r'^collect/teacher/$', UserCollectTeacherView.as_view(), name='user_collect_teacher'),

    # 用户收藏--课程页面
    url(r'^collect/course/$', UserCollectCourseView.as_view(), name='user_collect_course'),

    # 用户消息
    url(r'^message/$', UserMessageView.as_view(), name='user_message'),

    # 用户修改头像
    url(r'^image/upload/$', ImageUploadView.as_view(), name="image_upload"),

    # 用户修改密码
    url(r'^update/pwd/$', UserReSetPwdView.as_view(), name="reset_pwd"),

    # 发送邮件
    url(r'^send/email/$', SendCodeToEmailView.as_view(), name="send_email"),

    # 验证邮箱
    url(r'^verify/email/$', VerifyCodeView.as_view(), name="verify_code"),
]
