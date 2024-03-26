# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/23 20:31
# @File    : serializers.py.py
# @Software: PyCharm

from rest_framework import serializers

from .models import Users, Project, ProjectRolesUsers, Role


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        depth = 1
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        depth = 1
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        depth = 1
        fields = ('role_name',)


class ProjectRolesUsersSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    def get_role(self, ProjectRolesUsers):
        return ProjectRolesUsers.role.role_name

    def get_username(self, ProjectRolesUsers):
        return ProjectRolesUsers.users.username

    def get_display(self, ProjectRolesUsers):
        return ProjectRolesUsers.users.display

    def get_email(self, ProjectRolesUsers):
        return ProjectRolesUsers.users.email

    def get_phone(self, ProjectRolesUsers):
        return ProjectRolesUsers.users.phone

    class Meta:
        model = ProjectRolesUsers
        depth = 1
        fields = ('role', 'username', 'display', 'email', 'phone')
