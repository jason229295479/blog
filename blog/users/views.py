from django.shortcuts import render

# Create your views here.

from django.views import View


# 注册视图


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')


from django.http.response import HttpResponseBadRequest
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse


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
        redis_conn.setex('img::%s' % uuid, 300, text)
        # 5、返回图片二进制
        return HttpResponse(image, content_type='image/jpeg')
