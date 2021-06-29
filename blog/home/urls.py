# users子应用的视图路由
from django.urls import path

from home.views import IndexView

urlpatterns = [
    # 参数1 路由 参数2 视图函数名
    path('', IndexView.as_view(), name='index'),
]
