# users子应用的试图路由
from django.urls import path

from users.views import RegisterView, ImageCodeView, SmsCodeView

urlpatterns = [
    # 参数1 路由 参数2 视图函数名
    path('register/', RegisterView.as_view(), name='register'),
    # 添加图片验证码路由
    path('imagecode/', ImageCodeView.as_view(), name='imagecode'),
    # 添加短信验证码路由
    path('smscode/', SmsCodeView.as_view(), name='smscode'),
]
