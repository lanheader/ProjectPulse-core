# -*- coding: utf-8 -*-
# @Author  : LanJX
# @Email   : lanheader@163.com
# @Home    : https://www.cnblogs.com/lanheader/
# @Time    : 2024/3/22 23:55
# @File    : const.py
# @Software: PyCharm
from django.db import models


# 资源类型
class ResourceType(models.IntegerChoices):
    ECS = 1, "服务器"
    RDS = 2, "数据库"
    VPN = 3, "VPN"
    OSS = 4, "对象存储"
    MIDDLEWARE = 5, "中间件"


class DeployType(models.IntegerChoices):
    VM = 0, "虚拟机"
    container = 1, "容器"
