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
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("data", data.get("data")),
                ]
            )
        )
