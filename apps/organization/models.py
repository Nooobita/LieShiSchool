# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间" )

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

'''
    课程机构
'''


class CourseOrg(models.Model):

    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    category = models.CharField(max_length=20, choices=(('pxjg', u'培训机构'), ('gr', u"个人"), ('gx', '高校')),
                                verbose_name=u"机构类别", default=u'pxjg')
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"Logo")
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    tag = models.CharField(default='全国知名', max_length=10, verbose_name=u'机构标签')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    # 获取讲师的数目
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    # 定义在xadmin页面中显示的名称
    get_teacher_nums.short_description = u'教师数'

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_year = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name=u"头像", null=True, blank=True)
    points = models.CharField(default='', verbose_name=u"教学特点", max_length=50)
    age = models.IntegerField(default=0, verbose_name=u"讲师年龄")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程教师"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
