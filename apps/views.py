# Create your views here.

from rest_framework import permissions
from rest_framework import viewsets

from .models import Users
from .serializers import UserSerializer


class UserList(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Users.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
