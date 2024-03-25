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
from common.middleware.jwt import MyTokenObtainPairView
from common.views import get_user_info

router = routers.DefaultRouter()

router.register(r'users', views.UserList)
urlpatterns = [
    # 拼接路由路径
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain'),
    path('api/', include(router.urls)),
    path('console/user/info', get_user_info),

]
