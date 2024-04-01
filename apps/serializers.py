# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/23 20:31
# @File    : serializers.py.py
# @Software: PyCharm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from .models import Users, Project, ProjectRolesUsers, Role, Resource


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        with transaction.atomic():
            extra_data = dict()
            for field in ("groups", "user_permissions", "resource_group"):
                if field in validated_data.keys():
                    extra_data[field] = validated_data.pop(field)
            user = Users(**validated_data)
            user.set_password(validated_data["password"])
            user.save()
            for field in extra_data.keys():
                getattr(user, field).set(extra_data[field])
            return user

    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as msg:
            raise serializers.ValidationError(msg)
        return password

    class Meta:
        model = Users
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            "display": {"required": True},
        }


class UserDetailSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            elif attr in ("groups", "user_permissions", "resource_group"):
                getattr(instance, attr).set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as msg:
            raise serializers.ValidationError(msg)
        return password

    class Meta:
        model = Users
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "username": {"required": False},
        }


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        depth = 1
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        depth = 1
        fields = "__all__"


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
        user_id = validated_data.pop("user_id")
        role_id = validated_data.pop("role_id")
        project_id = validated_data.pop("project_id")
        if (
                ProjectRolesUsers.objects.filter(users__id=user_id)
                        .filter(role__id=role_id)
                        .filter(project__id=project_id)
                        .first()
        ):
            raise serializers.ValidationError("该项目用户角色已经存在！")

        user = Users.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)
        project = Project.objects.get(id=project_id)

        return ProjectRolesUsers.objects.create(
            users=user, role=role, project=project, **validated_data
        )

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
        fields = (
            "user_id",
            "role_id",
            "project_id",
            "id",
            "role",
            "username",
            "display",
            "email",
            "create_time",
            "update_time",
            "phone",
        )


class ResourceSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        project_id = validated_data.pop('project_id')
        project = Project.objects.get(id=project_id)
        # Assuming that you have access to request in the serializer context
        # and the user is attached to the request by Django authentication middleware
        user = self.context['request'].user
        return Resource.objects.create(creator=user, project=project, **validated_data)

    class Meta:
        model = Resource
        depth = 1
        fields = "__all__"
