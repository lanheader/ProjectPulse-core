from collections import OrderedDict

from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response


class CustomizedPagination(PageNumberPagination):
    """
    自定义分页器
    """

    page_size = (
        settings.REST_FRAMEWORK["PAGE_SIZE"]
        if "PAGE_SIZE" in settings.REST_FRAMEWORK.keys()
        else 20
    )
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = None

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", data.get("count", self.page.paginator.count)),
                    ("code", data.get("code", 20000)),
                    ("message", data.get("message", "success")),
                    ("status", data.get("status", 200)),
                    ("data_status", data.get("data_status", "success")),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("data", data.get("data")),
                ]
            )
        )


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
