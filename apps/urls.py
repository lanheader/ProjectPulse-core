# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/23 20:34
# @File    : urls.py.py
# @Software: PyCharm

from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from apps import views

router = routers.DefaultRouter()

router.register(r'users', views.UserList)
urlpatterns = [
    # 拼接路由路径
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 下面这个是用来验证token的，根据需要进行配置
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include(router.urls)),
    path(r'^api-auth/', include('rest_framework.urls',
                                namespace='rest_framework')),
]
