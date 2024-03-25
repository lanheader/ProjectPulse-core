# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/23 20:31
# @File    : serializers.py.py
# @Software: PyCharm

from rest_framework import serializers

from .models import Users, Project


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        depth = 1
        fields = '__all__'


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        depth = 1
        fields = '__all__'
