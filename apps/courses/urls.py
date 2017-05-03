# coding: utf-8
__author__ = 'nobita'
__date__ = '1/23/2017 10:41'

from django.conf.urls import url
from .views import CoursesListView, CoursesDetailView, CourseInfoView, CourseCommentView, \
    AddCourseCommentView, CoursePlayView


urlpatterns = [
    # 公开课展示列表
    url(r'^list/$', CoursesListView.as_view(), name="courses_list"),
    # 公开课详情页
    url(r'^detail/(?P<course_id>\d+)/$', CoursesDetailView.as_view(), name="courses_detail"),
    # 课程章节信息页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="courses_info"),
    # 课程评论页面
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    # 添加评论
    url(r'add_comment/$', AddCourseCommentView.as_view(), name="add_comment"),
    # 视频播放
    url(r'^video/(?P<video_id>\d+)/$', CoursePlayView.as_view(), name="course_video")

]

