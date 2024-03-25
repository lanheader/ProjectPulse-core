from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework_simplejwt import authentication

User = get_user_model()


def get_user_info(request):
    if request.method == 'GET':
        # print(dir(request))
        # 获取请求参数token的值
        token = request.headers.get('AUTHORIZATION')
        # test=request.META.get('CONTENT-TYPE')
        # print(test)
        # print(token)

        token_msg = authentication.JWTAuthentication().get_validated_token(token)
        user_object = authentication.JWTAuthentication().get_user(token_msg)
        if user_object.is_superuser:
            roles = ["admin"]
        else:
            roles = [0]
        data = {"username": user_object.username,
                "first_name": user_object.first_name,
                "last_name": user_object.last_name,
                "avatar": '',
                #  "groups":user_object.groups,
                "roles": roles,
                "introduction": ''
                }
        re_data = {"data": data,
                   "code": 20000,
                   "message": "success"
                   }
        return JsonResponse(re_data)
