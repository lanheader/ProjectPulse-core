# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/23 20:34
# @File    : urls.py.py
# @Software: PyCharm
from django.urls import path, include
from rest_framework import routers

from apps import views

router = routers.DefaultRouter()

router.register(r'users', views.UserList)
urlpatterns = [
    # 拼接路由路径
    path('api/', include(router.urls)),
    path(r'^api-auth/', include('rest_framework.urls',
                                namespace='rest_framework')),
]
