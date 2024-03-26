# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/25 17:27
# @File    : filter.py
# @Software: PyCharm
from django_filters import rest_framework as filters

from apps.models import Project, ProjectRolesUsers, Users, Role


class ProjectFilter(filters.FilterSet):
    class Meta:
        model = Project
        fields = {
            "id": ["exact"],
            "project_name": ["icontains"],
            "project_type": ["exact"],
            "project_code": ["icontains"],
            "description": ["icontains"],
            "create_time": ["exact"],
            "creator": ["exact"],
        }


class ProjectRolesUsersFilter(filters.FilterSet):
    class Meta:
        model = ProjectRolesUsers
        fields = {
            "id": ["exact"],
            "project": ["exact"],
            "role": ["exact"],
            "users": ["exact"],
            "create_time": ["exact"],
        }


class UsersFilter(filters.FilterSet):
    class Meta:
        model = Users
        fields = {
            "username": ["icontains"],
            "display": ["icontains"],
            "email": ["icontains"],
            "phone": ["icontains"],
            "date_joined": ["exact"],
            "is_active": ["exact"],
        }


class RoleFilter(filters.FilterSet):
    class Meta:
        model = Role
        fields = {
            "role_name": ["icontains"],
            "role_code": ["icontains"],
            "description": ["icontains"],
            "create_time": ["exact"],
            "creator": ["exact"],
        }
