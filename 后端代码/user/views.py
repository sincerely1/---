# Create your views here.
import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic.base import View
from rest_framework.authtoken.models import Token

from .auth import ExpiringTokenAuthentication
from .models import MyUser


class UserLoginView(View):
    def post(self, request):
        postBody = request.body
        data = json.loads(postBody)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user != None:
            login(request, user)
            try:
                tokenObj = Token.objects.get(user_id=user.id)
            except Exception as e:
                tokenObj = Token.objects.create(user=user)
            token = tokenObj.key

            res = {"code": 200, "message": "SUCCESS", "token": token}
            return JsonResponse(res)
        else:
            res = {"code": 60204, "message": "密码错误"}
            return JsonResponse(res)


class UserInfoView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        token = request.GET.get('token')
        if token != None:
            try:
                tokenObj = Token.objects.get(key=token)
                user_info = MyUser.objects.get(user=tokenObj.user.id)
            except Exception as e:
                res = {"code": 60203, "message": "输入错误信息用户不存在!"}
                return JsonResponse(res)
            data = {'account': user_info.user.username, 'name': user_info.true_name, 'role': [user_info.user_role],
                    'introduction': user_info.introduction, 'avatar': user_info.user_avatar,
                    'number': user_info.user_number}
            res = {"code": 200, "message": "SUCCESS", 'data': data}
            return JsonResponse(res)
        else:
            res = {"code": 50000, "message": "登陆超时，重新登陆!"}
            return JsonResponse(res)


class UserLogoutView(View):

    def get(self, request):
        token = request.GET.get('token')
        try:
            tokenObj = Token.objects.get(key=token)
            tokenObj.delete()
            res = {'code': 200, 'message': "登出成功"}
        except Exception as e:
            res = {'code': 60204, 'message': "登出失败"}
        return JsonResponse(res)


class GetUsersView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        # 这个只有管理员可以调用
        token = request.META.get('HTTP_X_TOKEN', b'')

        tokenObj = Token.objects.get(key=token)
        user_info = MyUser.objects.get(user=tokenObj.user.id)
        role = user_info.user_role
        if role != 'admin':
            res = {'code': 60204, 'message': "您不是管理员无权限查看"}
        else:
            users = MyUser.objects.exclude(user_role='admin')
            data = []
            for user_info in users:
                data.append(
                    {'account': user_info.user.username, 'name': user_info.true_name, 'role': user_info.user_role,
                     'introduction': user_info.introduction, 'number': user_info.user_number})
            res = {'code': 200, 'message': '获取成功', 'data': data}

        return JsonResponse(res)


class DelUserView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        # 这个只有管理员可以调用
        token = request.META.get('HTTP_X_TOKEN', b'')
        try:
            tokenObj = Token.objects.get(key=token)
            user_info = MyUser.objects.get(user=tokenObj.user.id)
            role = user_info.user_role
            if role != 'admin':
                res = {'code': 60204, 'message': "您不是管理员没有权限"}
            else:
                postBody = request.body
                data = json.loads(postBody)
                user = User.objects.get(username=data['account'])
                user.delete()
                res = {'code': 200, 'message': '删除成功'}
        except Exception as e:
            res = {'code': 60204, 'message': "服务器错误请检查输入数据"}
        return JsonResponse(res)


class AddUserView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        # 这个只有管理员可以调用
        token = request.META.get('HTTP_X_TOKEN', b'')
        try:
            tokenObj = Token.objects.get(key=token)
            user_info = MyUser.objects.get(user=tokenObj.user.id)
            role = user_info.user_role
            if role != 'admin':
                res = {'code': 60204, 'message': "您不是管理员没有权限"}
            else:
                post_body = request.body
                data = json.loads(post_body)
                user_info = MyUser.create_user(account=data['account'], true_name=data['name'],
                                               user_numbser=data['number'],
                                               user_role=data['role'], password=data['password'])
                if user_info != None:
                    data = {'account': user_info.user.username, 'name': user_info.true_name,
                            'role': user_info.user_role,
                            'introduction': user_info.introduction, 'number': user_info.user_number}
                    res = {'code': 200, 'message': '增加成功', 'data': data}
                else:
                    res = {'code': 50404, 'message': '用户已存在'}
        except Exception as e:
            print(e)
            res = {'code': 60204, 'message': "服务器错误请检查输入数据"}
        return JsonResponse(res)

class UpdateUserinfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)
    def post(self,request):
        postBody = request.body
        data = json.loads(postBody)
        token = request.META.get('HTTP_X_TOKEN', b'')
        try:
            tokenObj = Token.objects.get(key=token)
            user_info = MyUser.objects.get(user=tokenObj.user.id)
            user_info.user_number=data['userinfo']['number']
            user_info.true_name=data['userinfo']['name']
            user_info.introduction=data['userinfo']['introduction']
            password=data['userinfo']['password']
            if password!='':
                user_info.user.password=password
            user_info.save()
            res = {'code': 200, 'message': '修改成功'}
        except Exception as e:
            print(e)
            res = {'code': 60204, 'message': "服务器错误请检查是否输入合理数据"}
        return JsonResponse(res)
class UpdateUser(View):
    authentication_classes = (ExpiringTokenAuthentication,)
    def post(self,request):
        postBody = request.body
        data = json.loads(postBody)
        token = request.META.get('HTTP_X_TOKEN', b'')
        try:
            tokenObj = Token.objects.get(key=token)
            user_info = MyUser.objects.get(user=tokenObj.user.id)
            role = user_info.user_role
            if role != 'admin':
                res = {'code': 60204, 'message': "您不是管理员没有权限"}
            else:
                change_info = MyUser.objects.get(user=data['account'])
                change_info.user_role = data['role']
                change_info.true_name = data['name']
                change_info.save()
                res = {'code': 200, 'message': '修改成功'}
        except Exception as e:
            print(e)
            res = {'code': 60204, 'message': "服务器错误,请检查是否输入合理数据"}
        return JsonResponse(res)