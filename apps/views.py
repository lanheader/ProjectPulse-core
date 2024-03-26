# Create your views here.

from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.middleware.pagination import CustomizedPagination
from .filter import ProjectFilter, ProjectRolesUsersFilter, UsersFilter, RoleFilter
from .models import Users, Project, Role, ProjectRolesUsers
from .serializers import UserSerializer, ProjectSerializer, ProjectRolesUsersSerializer, RoleSerializer


class UserList(generics.ListAPIView):
    filterset_class = UsersFilter
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = Users.objects.all().order_by('-date_joined')
    pagination_class = CustomizedPagination

    @extend_schema(
        summary="项目清单",
        request=UserSerializer,
        responses={200: UserSerializer},
        description="列出所有项目（过滤，分页）",
    )
    def get(self, request):
        users = self.filter_queryset(self.queryset)
        page_ins = self.paginate_queryset(queryset=users)
        serializer_obj = self.get_serializer(page_ins, many=True)
        data = {
            "data": serializer_obj.data,
            "code": 20000,
            "msg": "获取成功",
            "status": 200,
            "data_status": "success"
        }
        return self.get_paginated_response(data=data)


class RoleList(generics.ListAPIView):
    filterset_class = RoleFilter
    permission_classes = [IsAuthenticated]
    serializer_class = RoleSerializer
    queryset = Role.objects.all().order_by('-create_time')
    pagination_class = CustomizedPagination

    @extend_schema(
        summary="角色列表",
        request=RoleSerializer,
        responses={200: RoleSerializer},
        description="列出所有角色（过滤，分页）",
    )
    def get(self, request):
        users = self.filter_queryset(self.queryset)
        page_ins = self.paginate_queryset(queryset=users)
        serializer_obj = self.get_serializer(page_ins, many=True)
        data = {
            "data": serializer_obj.data,
            "code": 20000,
            "message": "获取成功",
        }
        return self.get_paginated_response(data=data)


class ProjectList(generics.ListAPIView):
    filterset_class = ProjectFilter
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('-create_time')
    pagination_class = CustomizedPagination

    @extend_schema(
        summary="项目清单",
        request=ProjectSerializer,
        responses={200: ProjectSerializer},
        description="列出所有项目（过滤，分页）",
    )
    def get(self, request):
        projects = self.filter_queryset(self.queryset)
        page_ins = self.paginate_queryset(queryset=projects)
        serializer_obj = self.get_serializer(page_ins, many=True)
        data = {
            "data": serializer_obj.data,
            "code": 20000,
            "message": "获取成功",
        }
        return self.get_paginated_response(data=data)


class ProjectRolesUsersList(generics.ListAPIView):
    filterset_class = ProjectRolesUsersFilter
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectRolesUsersSerializer
    queryset = ProjectRolesUsers.objects.all().order_by('-create_time')
    pagination_class = CustomizedPagination

    @extend_schema(
        summary="项目角色清单",
        request=ProjectRolesUsersSerializer,
        responses={200: ProjectRolesUsersSerializer},
        description="列出项目下所有用户（过滤，分页）",
    )
    def get(self, request):
        projectUsers = self.filter_queryset(self.queryset)
        page_ins = self.paginate_queryset(queryset=projectUsers)
        serializer_obj = self.get_serializer(page_ins, many=True)
        data = {
            "data": serializer_obj.data,
            "code": 20000,
            "msg": "获取成功",
        }
        return self.get_paginated_response(data=data)

    @extend_schema(
        summary="创建项目角色",
        request=ProjectRolesUsersSerializer,
        responses={201: ProjectRolesUsersSerializer},
        description="创建一个项目角色",
    )
    def post(self, request):
        serializer = ProjectRolesUsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": serializer.data,
                "code": 20000,
                "message": "创建成功",
            }
            return Response(data=data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectRolesUsersDelete(generics.DestroyAPIView):
    queryset = ProjectRolesUsers.objects.all()
    serializer_class = ProjectRolesUsersSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Deleted successfully", "code": 20000})
