# Create your views here.

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.middleware.pagination import CustomizedPagination
from .filter import ProjectFilter, ProjectRolesUsersFilter, UsersFilter, RoleFilter, ResourceFilter
from .models import Users, Project, Role, ProjectRolesUsers, Resource
from .serializers import (
    UserSerializer,
    ProjectSerializer,
    ProjectRolesUsersSerializer,
    RoleSerializer,
    UserDetailSerializer,
    ResourceSerializer
)


class UserList(generics.ListAPIView):
    filterset_class = UsersFilter
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = Users.objects.all().order_by("-date_joined")
    pagination_class = CustomizedPagination

    @extend_schema(
        summary="项目用户",
        request=UserSerializer,
        responses={200: UserSerializer},
        description="列出所有用户（过滤，分页）",
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
            "data_status": "success",
        }
        return self.get_paginated_response(data=data)

    @extend_schema(
        summary="创建用户",
        request=UserSerializer,
        responses={201: UserSerializer},
        description="创建一个用户",
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(views.APIView):
    """
    用户操作
    """

    serializer_class = UserDetailSerializer

    def get_object(self, pk):
        try:
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="获取单条用户详细信息",
        request=UserDetailSerializer,
        responses={200: UserDetailSerializer},
        description="获取单条用户详细信息",
    )
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        summary="更新用户",
        request=UserDetailSerializer,
        responses={200: UserDetailSerializer},
        description="更新一个用户",
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="禁用用户", description="禁用一个用户")
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.is_active = not user.is_active
        user.save()
        serializer = UserDetailSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleList(generics.ListAPIView):
    filterset_class = RoleFilter
    permission_classes = [IsAuthenticated]
    serializer_class = RoleSerializer
    queryset = Role.objects.all().order_by("-create_time")
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
    queryset = Project.objects.all().order_by("-create_time")
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
    queryset = ProjectRolesUsers.objects.all().order_by("-create_time")
    pagination_class = CustomizedPagination

    @extend_schema(
        summary="项目角色清单",
        request=ProjectRolesUsersSerializer,
        responses={200: ProjectRolesUsersSerializer},
        description="列出项目下所有用户（过滤，分页）",
    )
    def get(self, request):
        project_id = request.query_params.get('project_id')
        if project_id is not None:
            self.queryset = self.queryset.filter(project__id=project_id)
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

    @extend_schema(
        summary="删除项目角色",
        request=ProjectRolesUsersSerializer,
        responses={201: ProjectRolesUsersSerializer},
        description="删除项目角色",
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Deleted successfully", "code": 20000})


class ResourceList(generics.ListAPIView):
    filterset_class = ResourceFilter
    permission_classes = [IsAuthenticated]
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all().order_by("-create_time")
    pagination_class = CustomizedPagination

    @extend_schema(
        summary="资源列表",
        request=ResourceSerializer,
        responses={200: ResourceSerializer},
        description="列出所有资源（过滤，分页），如ECS，RDS等",
    )
    def get(self, request):
        project_id = request.query_params.get('project_id')
        if project_id is not None:
            self.queryset = self.queryset.filter(project__id=project_id)
        resource = self.filter_queryset(self.queryset)
        page_ins = self.paginate_queryset(queryset=resource)
        serializer_obj = self.get_serializer(page_ins, many=True)
        data = {
            "data": serializer_obj.data,
            "code": 20000,
            "msg": "获取成功",
            "status": 200,
            "data_status": "success",
        }
        return self.get_paginated_response(data=data)

    @extend_schema(
        summary="创建资源",
        request=ResourceSerializer,
        responses={201: ResourceSerializer},
        description="创建一个资源",
    )
    def post(self, request):
        serializer = ResourceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(serializer.errors)
