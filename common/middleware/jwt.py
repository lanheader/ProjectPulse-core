# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/24 00:00
# @File    : auth.py
# @Software: PyCharm

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        # token['username'] = user.username
        # token['code'] = 20000
        # print(token)
        # ... 官方示例中上面的部分没有生效
        # print(token)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        re_data = {'data': data, 'code': 20000, 'message': 'success'}
        return re_data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
