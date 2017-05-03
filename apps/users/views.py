# coding: utf-8
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from .forms import LoginForms, RegisterForms, ForgetForms, ModifyForms, ModifyUserForms, ImageUploadForms
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from django.http import HttpResponse, HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course
from users.models import Banner
from organization.models import CourseOrg, Teacher
from MxOnline.settings import MEDIA_ROOT
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
import os
import json
# 重写django默认的登陆验证


class CustomBakend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 修改密码
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyForms(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')
            email = request.POST.get("email", '')
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "两次密码不一致!"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", '')
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


# 重置密码
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return HttpResponse("重置密码失败!")


# 忘记密码
class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForms()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForms(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, send_type='forget')
            return HttpResponse("邮件已经发送! 注意查收!")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


# 激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return HttpResponse("链接失效")
        return render(request, "login.html", {})


# 注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForms()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForms(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "改用户已经注册!"})
            else:
                user_pwd = request.POST.get('password', '')
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.is_active = False
                user_profile.password = make_password(user_pwd)
                user_profile.save()
                # 发送信息
                user_message = UserMessage()
                user_message.user = user_profile.id
                user_message.message = "欢迎注册幕学网!"
                user_message.save()

                send_register_email(user_name, send_type='register')
                return render(request, 'login.html', {})
        else:
            return render(request, "register.html", {"register_form": register_form})


# 类方式定义视图(常用)
# 登陆

class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", '')
            user_pwd = request.POST.get("password", '')
            user = authenticate(username=user_name, password=user_pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": "请激活用户再登陆!"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_form": login_form})


# 注销

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 用户中心首页
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {
            "current_page": 'info'
        })

    def post(self, request):
        user_form = ModifyUserForms(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure","msg":"信息保存失败"}', content_type='application/json')


# 用户我的课程页面
class UserCourseView(LoginRequiredMixin, View):
    def get(self, request):
        courses = UserCourse.objects.filter(user=request.user)
        course_id = [course.course.id for course in courses]
        all_courses = Course.objects.filter(id__in=course_id)
        return render(request, 'usercenter-mycourse.html', {
            "all_courses": all_courses,
            "current_page": "course"
        })


# 用户收藏--机构
class UserCollectOrgView(LoginRequiredMixin, View):
    def get(self, request):
        user_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        org_id = [user_fav_org.fav_id for user_fav_org in user_fav_orgs]
        orgs = CourseOrg.objects.filter(id__in=org_id)
        return render(request, 'usercenter-fav-org.html', {
            "current_page": "collect",
            "orgs": orgs
        })


# 用户收藏--讲师
class UserCollectTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        user_fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teacher_id = [user_fav_teacher.fav_id for user_fav_teacher in user_fav_teachers]
        teachers = Teacher.objects.filter(id__in=teacher_id)
        return render(request, 'usercenter-fav-teacher.html', {
            "current_page": "collect",
            "teachers": teachers
        })


# 用户收藏--课程
class UserCollectCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        course_id = [user_fav_course.fav_id for user_fav_course in user_fav_courses]
        courses = Course.objects.filter(id__in=course_id)
        return render(request, 'usercenter-fav-course.html', {
            "current_page": "collect",
            "courses": courses
        })


# 用户消息
class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        user_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation
        # 控制每一页显示的个数
        p = Paginator(user_messages, 5, request=request)

        user_messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "user_messages": user_messages,
            "current_page": "message",
        })


# 用户修改头像
class ImageUploadView(View):
    def post(self, request):

        # 要在image_form前记录,
        # image_form后记录,request.user.image,中的地址会改变,然后save()再写入数据库

        old_image_path = request.user.image
        image_form = ImageUploadForms(request.POST, request.FILES, instance=request.user)

        if image_form.is_valid():
            # 删除旧的图片
            old_image = os.path.join(MEDIA_ROOT, str(old_image_path))
            if os.path.exists(old_image):
                os.remove(old_image)
            image_form.save(commit=True)
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail'}", content_type='application/json')


# 用户修改密码

class UserReSetPwdView(View):
    def post(self, request):
        modify_form = ModifyForms(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"两次密码不一致"}', content_type='application/json')
            else:
                user = request.user
                user.password = make_password(pwd2)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


# 发送验证码到邮箱

class SendCodeToEmailView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        else:
            if send_register_email(email, send_type='modify_email'):
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failure"}', content_type='application/json')


# 验证验证码修改邮箱
class VerifyCodeView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        exist_code = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="modify_email")
        if exist_code:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错!"}', content_type='application/json')


# 首页
class IndexView(View):
    def get(self, request):

        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        courses = Course.objects.filter(is_banner=False).order_by('-students')[:6]
        course_orgs = CourseOrg.objects.all()[:15]

        return  render(request, 'index.html', {
            "all_banners": all_banners,
            "banner_courses": banner_courses,
            "courses": courses,
            "course_orgs": course_orgs
        })


# 404错误页面
def page_not_found(request):
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response


# 500错误页面
def page_error(request):
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response


# 403错误页面
def page_forbidden(request):
    response = render_to_response('403.html',{})
    response.status_code = 403
    return response


# 函数方式定义视图
def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username', '')
        user_pwd = request.POST.get('password', '')
        user = authenticate(username=user_name, password=user_pwd)
        if user is not None:
            login(request, user)
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误!"})
    elif request.method == 'GET':
        return render(request, "login.html", {})
