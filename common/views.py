from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework_simplejwt import authentication

User = get_user_model()


def get_user_info(request):
    if request.method == "GET":
        auth = authentication.JWTAuthentication()
        header = auth.get_header(request)
        raw_token = auth.get_raw_token(header)
        validated_token = auth.get_validated_token(raw_token)
        user_object = auth.get_user(validated_token)
        if user_object.is_superuser:
            roles = ["admin"]
        else:
            roles = [0]
        data = {
            "username": user_object.username,
            "first_name": user_object.first_name,
            "last_name": user_object.last_name,
            "avatar": "",
            #  "groups":user_object.groups,
            "roles": roles,
            "introduction": "",
        }
        re_data = {"data": data, "code": 20000, "message": "success"}
        return JsonResponse(re_data)
