# coding: utf-8
__author__ = 'nobita'
__date__ = '1/21/2017 00:20'
from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfJjHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register", ):
    email_record = EmailVerifyRecord()
    if send_type == 'modify_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.send_type = send_type
    email_record.email = email
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = u"幕学网在线网站注册激活链接"
        email_body = u"请点击下面的链接激活您的账号 http://127.0.0.1:8000/active/{0}".format(code)
    elif send_type == "forget":
        email_title = u"幕学网在线网站忘记密码链接"
        email_body = u"请点击下面的链接找回您的账号 http://127.0.0.1:8000/reset/{0}".format(code)
    elif send_type == "modify_email":
        email_title = u"幕学网在线网站修改邮箱验证码"
        email_body = u"本次验证码为{0}，请不要告诉别人".format(code)

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

    return send_status
