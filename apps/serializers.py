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


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        depth = 1
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        depth = 1
        fields = '__all__'


class ProjectRolesUsersSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(write_only=True)
    role_id = serializers.IntegerField(write_only=True)
    project_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        role_id = validated_data.pop('role_id')
        project_id = validated_data.pop('project_id')
        if (ProjectRolesUsers.objects.
                filter(users__id=user_id).
                filter(role__id=role_id).
                filter(project__id=project_id).
                first()):
            raise serializers.ValidationError('该项目用户角色已经存在！')

        user = Users.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)
        project = Project.objects.get(id=project_id)

        return ProjectRolesUsers.objects.create(users=user, role=role, project=project, **validated_data)

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
        fields = ('user_id', 'role_id', 'project_id', 'id', 'role', 'username', 'display', 'email', 'phone')
