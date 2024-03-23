# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/22 22:56
# @File    : form.py
# @Software: PyCharm

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import ModelForm

from .models import Users


class GroupForm(ModelForm):
    users = forms.ModelMultipleChoiceField(
        label="用户",
        queryset=Users.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("用户", is_stacked=False),
    )

    class Meta:
        model = Group
        exclude = ()  # since Django 1.8 this is needed
        widgets = {
            "permissions": admin.widgets.FilteredSelectMultiple(
                "permissions", is_stacked=False
            ),
        }
