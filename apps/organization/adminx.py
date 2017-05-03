# coding: utf-8
__author__ = 'nobita'
__date__ = '1/20/2017 00:55'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-map-o'
    exclude = ('add_time',)
    list_per_page = 10
    relfield_style = 'fk-ajax'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums',
                    'address', 'city', 'get_teacher_nums', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image',
                     'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image',
                   'address', 'city', 'add_time']
    model_icon = 'fa fa-address-card'
    exclude = ('add_time', 'click_nums', 'fav_nums', 'students')
    list_per_page = 10
    list_editable = ['name']
    # relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points',
                    'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points',
                     'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points',
                   'click_nums', 'fav_nums', 'add_time']
    model_icon = 'fa fa-odnoklassniki'
    exclude = ('add_time', 'click_nums', 'fav_nums')
    list_per_page = 10
    list_editable = ['name', 'work_year', 'work_company', 'work_position', 'points']
    # relfield_style = 'fk-ajax'


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
