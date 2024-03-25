# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/24 00:31
# @File    : res.py
# @Software: PyCharm
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, data_status, data_code, msg='', data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        data = {
            'status': data_status,
            'code': data_code,
            'msg': msg,
            'data': data,
        }
        super().__init__(data=data, status=status,
                         template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)
