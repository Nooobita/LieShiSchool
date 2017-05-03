# coding: utf-8

from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict, Teacher
from operation.models import UserFavorite
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddUserAskForm
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q
from courses.models import Course
# Create your views here


# 课程机构列表功能
class OrgView(View):
    def get(self, request):
        # 机构
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        # 热门机构
        host_orgs = all_orgs.order_by("-click_nums")[:3]
        # 城市
        all_citys = CityDict.objects.all()

        # 主页课程机构搜索功能
        keywords = request.GET.get("keywords", '')
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 取出筛选城市
        city_id = request.GET.get('city', 'all')
        # 取出筛选类别
        category = request.GET.get('ct', 'all')
        # 取出筛选条件
        sort = request.GET.get('sort', 'all')

        if city_id != "all":
            all_orgs = all_orgs.filter(city_id=int(city_id))
        if category != "all":
            all_orgs = all_orgs.filter(category=category)
        if sort != "all":
            if sort == 'students':
                all_orgs = all_orgs.order_by("-students")
            elif sort == 'courses':
                all_orgs = all_orgs.order_by("-course_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "city_id": city_id,
            "category": category,
            "sort": sort,
            "host_orgs": host_orgs,
            "org_nums": org_nums
        })


# 用户咨询
class AddUserAskView(View):
    def post(self, request):
        user_ask_form = AddUserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg": "信息有误!"}', content_type="application/json")


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teachers": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


# 机构课程列表
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation
        # 控制每一页显示的个数
        p = Paginator(all_courses, 5, request=request)

        courses = p.page(page)

        return render(request, 'org-detail-course.html', {
            "courses": courses,
            "current_page": current_page,
            "course_org": course_org,
            "has_fav": has_fav
        })


# 机构介绍
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


# 机构教师
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {
            "current_page": current_page,
            "course_org": course_org,
            "teachers": all_teachers,
            "has_fav": has_fav
        })


# 用户收藏 用户取消收藏
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        # 判断用户登陆状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg":"用户未登陆"}', content_type="application/json")
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在,则表示用户取消收藏
            exist_records.delete()
            # 收藏数
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            if fav_id > 0 and fav_type >0:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    if course_org.fav_nums < 0:
                        course_org.fav_nums = 0
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()

                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


# 讲师列表页面
class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teacher_ranges = all_teachers.order_by("-fav_nums")[:3]

        # 主页讲师搜索功能
        keywords = request.GET.get("keywords", '')
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords) |
                                               Q(work_company__icontains=keywords) |
                                               Q(work_position__icontains=keywords))

        # 筛选功能
        sort = request.GET.get('sort', '')

        if sort == "hot":
            all_teachers.order_by('-fav_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation
        # 控制每一页显示的个数
        p = Paginator(all_teachers, 3, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            "all_teachers": teachers,
            "teacher_num": all_teachers.count,
            "teacher_ranges": teacher_ranges,
            "sort": sort
        })


# 讲师详情页
class TeacherDetailView(LoginRequiredMixin, View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        teacher_ranges = Teacher.objects.all().order_by('-fav_nums')[:3]
        courses = teacher.course_set.all()

        # 检查收藏按钮
        has_teacher_fav = False
        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
            has_teacher_fav = True
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
            has_org_fav = True

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation
        # 控制每一页显示的个数
        p = Paginator(courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'teacher-detail.html', {
            "teacher": teacher,
            "teacher_ranges": teacher_ranges,
            "courses": courses,
            "has_teacher_fav": has_teacher_fav,
            "has_org_fav": has_org_fav
        })
