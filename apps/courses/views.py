# coding: utf-8
from django.shortcuts import render
from django.views.generic import View
from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q
# Create your views here.


# 公开课列表
class CoursesListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        host_courses = all_courses.order_by("-click_nums")[:3]

        # 主页公开课搜索功能
        keywords = request.GET.get("keywords", '')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) |
                                             Q(desc__icontains=keywords) |
                                             Q(detail__icontains=keywords))

        # 筛选功能
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_courses = all_courses.order_by("-students")
        elif sort == 'hot':
            all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation
        # 控制每一页显示的个数
        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "host_courses": host_courses,
            "sort": sort,
        })


# 公开课详情页
class CoursesDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 记录课程标签, 用于找想相关课程
        tag = course.tag
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []

        # 收藏按钮操作
        has_course_fav = False
        has_org_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_course_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_org_fav = True

        return render(request, "course-detail.html", {
            "course": course,
            "relate_course": relate_course,
            "has_course_fav": has_course_fav,
            "has_org_fav": has_org_fav
        })


# 课程信息页面(章节信息)
# 继承LoginRequiredMixin(通过装饰器来实现),验证用户是否登录
class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询用户是否已经关联了该课程
        user_cou = UserCourse.objects.filter(user=request.user, course=course)
        if not user_cou:
            user_cou = UserCourse(user=request.user, course=course)
            user_cou.save()
            # 课程人数增加
            course.students += 1
            course.save()

        # 学过该课程的用户还学过什么课程
        # 思路:
        # 通过'课程',找到学习过该课程的所有用户
        # 通过'用户课程'中间表找到所有用户的ID
        # 通过'用户ID',找到这些用户都学习过什么课程
        # 然后找到课程ID，通过ID查找课程表，找到课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # user_id__in -> user对象的id(调用外键的属性方法:user_id),并调用in方法
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course=course)
        course_ids = [course_id.course.id for course_id in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:2]

        # 获得资源对象
        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            "course": course,
            "all_resource": all_resource,
            "relate_courses": relate_courses
        })


# 课程评论页面
class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_resource = CourseResource.objects.filter(course=course)
        comments = CourseComments.objects.filter(course=course).order_by('-add_time')

        # 学过该课程的用户还学过什么课程
        user_course = UserCourse.objects.filter(course=course)
        user_ids = [user.user.id for user in user_course]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course=course)
        course_ids = [course_id.course.id for course_id in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:2]

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation
        # 控制每一页显示的个数
        p = Paginator(comments, 1, request=request)

        comments = p.page(page)

        return render(request, 'course-comment.html', {
            "course": course,
            "comments": comments,
            "all_resource": all_resource,
            "relate_courses": relate_courses
        })


# 添加课程评论
class AddCourseCommentView(View):
    def post(self, request):
        # 判断用户是否登
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登陆"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comment = request.POST.get("comments", "")
        if course_id >0 and comment:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comment
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type="application/json")


# 课程视频播放页面
class CoursePlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        # 学过该课程的用户还学过什么课程
        # 思路:
        # 通过'课程',找到学习过该课程的所有用户
        # 通过'用户课程'中间表找到所有用户的ID
        # 通过'用户ID',找到这些用户都学习过什么课程
        # 然后找到课程ID，通过ID查找课程表，找到课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # user_id__in -> user对象的id(调用外键的属性方法:user_id),并调用in方法
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course=course)
        course_ids = [course_id.course.id for course_id in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:2]

        # 获得资源对象
        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            "course": course,
            "all_resource": all_resource,
            "relate_courses": relate_courses,
            'video': video
        })
