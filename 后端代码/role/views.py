from django.shortcuts import render

# Create your views here.
from user.auth import ExpiringTokenAuthentication
from django.views.generic.base import View
from django.http import JsonResponse

class RolesView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        #返回角色列表，不包含admin管理员
        res={'code':200,'message':'获取成功','data':[{'key':'teacher','name':'teacher'},{'key':'student','name':'student'}]}
        return JsonResponse(res)