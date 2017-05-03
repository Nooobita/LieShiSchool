# coding:utf-8

from __future__ import unicode_literals
from datetime import datetime
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField

# django框架
from django.db import models


# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", default='')
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=200, verbose_name=u"课程描述")
    course_teacher = models.ForeignKey(Teacher, verbose_name=u"课程教师", default='')
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=5, verbose_name=u'课程难度')
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图片")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(max_length=20, verbose_name=u"课程类别", default='')
    tag = models.CharField(max_length=20, verbose_name=u"课程标签", default='')
    course_need_konow = models.CharField(max_length=200, verbose_name=u"课程须知", default='')
    course_you_learn = models.CharField(max_length=200, verbose_name=u"学到知识", default='')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="course/ueditor/%(datetime)/",
                          filePath="course/ueditor/%(datetime)/", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    # 获得章节数
    def get_lessons(self):
        return self.lesson_set.all().count()

    # 定义该函数在xadmin中显示的名称
    get_lessons.short_description = u"章节数"

    # 获得资源数
    def get_resource_nums(self):
        return self.courseresource_set.all().count()

    # 定义在xadmin中显示的名称
    get_resource_nums.short_description = u'资源数'


    # 获得章节
    def get_lesson(self):
        return self.lesson_set.all()

    # 获得用户信息
    def get_students(self):
        return self.usercourse_set.all()[:4]

    # 获得用户学习数量
    def get_student_nums(self):
        return self.usercourse_set.all().count()

    # 获得课程数
    def get_course_nums(self):
        return self.course_org.course_set.all().count()

    # 获得教师数
    def get_teacher_nums(self):
        return self.course_org.teacher_set.all().count()

    def __unicode__(self):
        return self.name


class BannerCourse(Course):

    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name

        # 很重要,有了这个参数就不会创建表
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    # 获取视频信息
    def get_videos(self):
        return self.video_set.all()

    # 获取视频数量
    def get_video_nums(self):
        return self.video_set.all().count()

    # 定义函数在xadmin中显示的名称
    get_video_nums.short_description = '视频数'


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    learn_time = models.CharField(max_length=20, verbose_name=u"学习时长", default='')
    video_url = models.URLField(max_length=200, verbose_name=u"视频链接", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"资源名")
    download = models.FileField(upload_to="course/resource/%Y%m", verbose_name=u"资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
