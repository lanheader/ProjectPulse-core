from django.contrib.auth.backends import ModelBackend

from apps.models import Users


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 添加了一个手机验证，如果需要其他验证再加
            user = Users.objects.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None
