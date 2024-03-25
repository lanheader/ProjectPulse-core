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


# 登录过期时 自定义 返回
class ExceptionChange:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if hasattr(response, 'data'):
            data = response.data
            if isinstance(data, dict) is True:
                if "detail" in data.keys():
                    # 用户名或密码错误
                    if data.get("detail") == "找不到指定凭据对应的有效用户":
                        del response.data["detail"]
                        response.data["code"] = 402
                        response.data["msg"] = "用户名或者密码错误!"

                    # 验证信息过期 token 过期
                    if data.get("detail") == "此令牌对任何类型的令牌无效":
                        del response.data["detail"]
                        del response.data["messages"]
                        response.data["code"] = 401
                        response.data["msg"] = "登录已过期，请重新登录"

                    # 未使用验证信息 未带验证信息请求
                    if data.get("detail") == "身份认证信息未提供。":  # 身份认证信息未提供。
                        del response.data["detail"]
                        response.data["code"] = 401
                        response.data["msg"] = "登录已过期，请重新登录"

                    # refresh 无效或者过期
                    if data.get("detail") == "令牌无效或已过期":  # 身份认证信息未提供。
                        del response.data["detail"]
                        response.data["code"] = 403
                        response.data["msg"] = "令牌无效或已过期"

        return response
