# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/25 17:27
# @File    : filter.py
# @Software: PyCharm
from django_filters import rest_framework as filters

from apps.models import Project, ProjectRolesUsers


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

        }
