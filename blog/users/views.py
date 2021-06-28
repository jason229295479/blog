import re

from django.shortcuts import render

# Create your views here.

from django.views import View

# 注册视图

import re
from users.models import User
from django.db import DatabaseError
# 验证码视图
from django.http.response import HttpResponseBadRequest
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse

# 短信验证视图
from django.http import JsonResponse
from utils.response_code import RETCODE
import logging

logger = logging.getLogger('django')
from random import randint
from libs.yuntongxun import send_sms


# 注册视图
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 1.接受数据
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        smscode = request.POST.get('sms_code')

        # 2.验证数据
        # 2.1参数是否齐全
        if not all([mobile, password, password2, smscode]):
            return HttpResponseBadRequest('缺少必要的参数')
        # 2.2手机格式是否正确 使用正则表达式
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号不符合规则')
        if User.objects.filter(username=mobile):
            return HttpResponseBadRequest('用户已经存在，请直接登录')
        # 2.3密码是否符合格式
        if not re.match(r'^[0-9A-Za-z]{8,50}$', password):
            return HttpResponseBadRequest('请输入8-20位密码，密码是数字，字母')
        # 2.4密码和确认密码是否一致
        if password != password2:
            return HttpResponseBadRequest('密码不一致')
        # 2.5短信验证码是否和redis中的一致
        redis_conn = get_redis_connection('default')
        redis_sms_code = redis_conn.get('sms:%s' % mobile)
        if redis_sms_code is None:
            return HttpResponseBadRequest('短信验证码过期')
        if smscode != redis_sms_code.decode():
            return HttpResponseBadRequest('短信验证码不一致')
        # 3.保存注册信息
        # create_user() 可以使用系统的方法来对密码进行加密

        try:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        except DatabaseError as e:
            logger.error(e)
            return HttpResponseBadRequest('注册失败')
        # 4.返回响应跳转指定页面
        return HttpResponse('注册成功，重定向到首页')


# 验证码视图
class ImageCodeView(View):
    def get(self, request):
        """
        ：param request
        :return
        """
        # 1、接受前端传递的uuid
        uuid = request.GET.get('uuid')
        # 2、判断uuid是否获取到
        if uuid is None:
            return HttpResponseBadRequest('没有传递uuid')
        # 3、通过调用的captcha 来生成图片验证码（图片二进制和图片内容）
        text, image = captcha.generate_captcha()
        # 4、将图片内容保持到redis中 0号库
        #     uuid为key 图片类容为value 同时设置时效
        redis_conn = get_redis_connection('default')
        """
        def setex(self, name, time, value):
        """
        redis_conn.setex('img:%s' % uuid, 300, text)
        # 5、返回图片二进制
        return HttpResponse(image, content_type='image/jpeg')


# 短信验证视图
class SmsCodeView(View):
    def get(self, request):
        # 1接收参数 查询传递过来的字符串的形式
        mobile = request.GET.get('mobile')
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 2验证参数
        # 2.1验证参数是否齐全
        if not all([mobile, image_code, uuid]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必要的参数'})
        # 2.2图片验证码
        # 连接redis中的图片验证码
        redis_conn = get_redis_connection('default')
        redis_image_code = redis_conn.get('img:%s' % uuid)
        # 判断图片验证码是否存在
        if redis_image_code is None:
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图片验证码已过期'})
        # 如果图片验证码未过期，则获取之后就可以删除图片验证码
        try:
            redis_conn.delete('img:%s' % uuid)
        except Exception as e:
            logger.error(e)
        # 比对图片验证码，注意的大小写，redis的数据类型是bytes类型
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图片验证错误'})
        # 3.生成短信验证码 随机生成6位
        sms_code = '%06d' % randint(0, 999999)
        # 为了后期比对方便，我们可以将短信验证码记录到日志中
        logger.info(sms_code)
        # 4.保存短信验证码到redis中
        redis_conn.setex('sms:%s' % mobile, 300, sms_code)
        # 5.发送短信
        send_sms(mobile, [sms_code, 5], 1)
        # 6.返回响应
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '短信发送成功'})
