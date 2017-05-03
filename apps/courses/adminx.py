# coding: utf-8
__author__ = 'nobita'
__date__ = '1/20/2017 00:12'

import xadmin
from .models import Course, Lesson, Video, CourseResource, BannerCourse


# 设置连接添加, 设置后可以在课程中直接添加章节信息，但不能不嵌套添加，也就是说不能添加视频信息

class CourseResourceInLine(object):
    model = CourseResource
    extra = 0


class LessonInLine(object):
    model = Lesson
    extra = 0


class VideoInLine(object):
    model = Video
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'course_org', 'course_teacher', 'degree', 'learn_times',
                    'students', 'fav_nums', 'click_nums', 'get_lessons', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'course_org', 'degree', 'learn_times', 'students',
                     'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'course_org', 'degree', 'learn_times', 'students',
                   'fav_nums', 'click_nums', 'add_time']
    model_icon = 'fa fa-desktop'
    ordering = ['-students']
    exclude = ('fav_nums', 'click_nums', 'add_time', 'students')
    list_per_page = 5
    list_editable = ['name']
    inlines = [LessonInLine, CourseResourceInLine]
    relfield_style = 'fk-ajax'
    refresh_times = [5, 10]  # 自动刷新设置
    style_fields = {"detail": "ueditor"}

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 保存课程的时候统计课程机构的课程数
    '''
        def save_model(self):
            obj = self.new_obj
            obj.save()
            if obj.course_org is not None：
                course_org = obj.course_org
                course_org.course_nums = Course.objects.filter(course_org=course_org).count()+1
                course_org.save()
    '''
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        # 重写post函数后，一定要返回，不然会出错
        return super(CourseAdmin, self).post(request, *args, **kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'course_org', 'course_teacher', 'degree', 'learn_times',
                    'students', 'fav_nums', 'click_nums', 'get_lessons', 'get_resource_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'course_org', 'degree', 'learn_times', 'students',
                     'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'course_org', 'degree', 'learn_times', 'students',
                   'fav_nums', 'click_nums', 'add_time']
    model_icon = 'fa fa-file-image-o'
    ordering = ['-students']
    exclude = ('fav_nums', 'click_nums', 'add_time')
    inlines = [LessonInLine, CourseResourceInLine]
    list_per_page = 5
    relfield_style = 'fk-ajax'
    style_fields = {"detail": "ueditor"}
    list_editable = ['name']

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'get_video_nums', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fa fa-window-restore'
    exclude = ('add_time',)
    list_per_page = 5
    list_editable = 'name'
    inlines = [VideoInLine]
    relfield_style = 'fk-ajax'


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']
    list_editable = ['name']
    model_icon = 'fa fa-youtube-play'
    exclude = ('add_time', )
    list_per_page = 5
    relfield_style = 'fk-ajax'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']
    model_icon = 'fa fa-file-text-o'
    exclude = ('add_time', )
    list_per_page = 5
    list_editable = ['name']
    relfield_style = 'fk-ajax'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
