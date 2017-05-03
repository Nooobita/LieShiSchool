# coding: utf-8
__author__ = 'nobita'
__date__ = '1/22/2017 15:23'

from django.conf.urls import url
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, \
    OrgDescView, OrgTeacherView, AddFavView, TeacherListView, TeacherDetailView


urlpatterns = [
    # 课程机构列表
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    # 添加用户咨询
    url(r'^userAsk/$', AddUserAskView.as_view(), name='org_userAsk'),
    # 机构主页
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    # 机构课程列表
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    # 机构介绍
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    # 机构教师
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),

    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    # 讲师列表
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    # 讲师详情页面
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail')
]
