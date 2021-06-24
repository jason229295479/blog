# users子应用的试图路由
from django.urls import path

from users.views import RegisterView

urlpatterns = [
    # 参数1 路由 参数2 视图函数名
    path('register/', RegisterView.as_view(), name='register'),
]
