# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/23 20:34
# @File    : urls.py.py
# @Software: PyCharm

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers

from apps import views
from common.middleware.jwt import MyTokenObtainPairView
from common.views import get_user_info

router = routers.DefaultRouter()
urlpatterns = [
    # 拼接路由路径
    path("login", MyTokenObtainPairView.as_view(), name="token_obtain"),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # schema的配置文件的路由，下面两个ui也是根据这个配置文件来生成的
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger-ui的路由
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # redoc的路由
    path("user/info", get_user_info),
    path("project", views.ProjectList.as_view(), name="project_list"),
    path("users", views.UserList.as_view(), name="user_list"),
    path("users/<int:pk>", views.UserDetail.as_view()),
    path("role", views.RoleList.as_view(), name="role_list"),
    path(
        "projectUsers", views.ProjectRolesUsersList.as_view(), name="projectUser_list"
    ),
    path(
        "projectrolesusers/<int:pk>",
        views.ProjectRolesUsersDelete.as_view(),
        name="projectRolesUsers_delete",
    ),
    path("resource", views.ResourceList.as_view(), name="resource_list"),
]
