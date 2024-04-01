# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/26 16:25
# @File    : customrenderer.py
# @Software: PyCharm

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.views import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return Response(
            {"message": "{exc}".format(exc=exc)},
            status=status.HTTP_200_OK,
            exception=True,
        )

    else:
        return Response(
            {
                "message": "{exc}".format(exc=exc),
            },
            status=status.HTTP_200_OK,
            exception=True,
        )


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if isinstance(data, dict):
                msg = data.pop("message", "请求成功")
                code = data.pop("code", 20000)
            else:
                msg = "请求成功"
                code = 20000
            ret = {
                "message": msg,
                "code": code,
                "data": data,
            }
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
