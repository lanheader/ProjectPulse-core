# Create your views here.

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from common.middleware.res import CustomResponse
from .filter import ProjectFilter, ProjectRolesUsersFilter
from .models import Users, Project, ProjectRolesUsers
from .serializers import UserSerializer, ProjectSerializer, ProjectRolesUsersSerializer


class UserList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ProjectList(generics.ListAPIView):
    filterset_class = ProjectFilter
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('-create_time')

    @extend_schema(
        summary="项目清单",
        request=ProjectSerializer,
        responses={200: ProjectSerializer},
        description="列出所有项目（过滤，分页）",
    )
    def get(self, request):
        instances = self.filter_queryset(self.queryset)
        page_ins = self.paginate_queryset(queryset=instances)
        serializer_obj = self.get_serializer(page_ins, many=True)
        data = serializer_obj.data
        return CustomResponse(data=data, data_code=20000, msg="获取成功", status=200, data_status="success")


class ProjectRolesUsersList(generics.ListAPIView):
    filterset_class = ProjectRolesUsersFilter
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectRolesUsersSerializer
    queryset = ProjectRolesUsers.objects.all().order_by('-create_time')

    @extend_schema(
        summary="项目角色清单",
        request=ProjectSerializer,
        responses={200: ProjectSerializer},
        description="列出项目下所有用户（过滤，分页）",
    )
    def get(self, request):
        instances = self.filter_queryset(self.queryset)
        page_ins = self.paginate_queryset(queryset=instances)
        serializer_obj = self.get_serializer(page_ins, many=True)
        data = serializer_obj.data
        return CustomResponse(data=data, data_code=20000, msg="获取成功", status=200, data_status="success")
