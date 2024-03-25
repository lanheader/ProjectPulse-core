# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Users, Project
from .serializers import UserSerializer, ProjectSerializer


class UserList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ProjectList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all().order_by('-create_time')
    serializer_class = ProjectSerializer
