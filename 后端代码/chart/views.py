from django.http import JsonResponse
from django.views.generic.base import View

from chart.utils import *
from course.models import Course
from user.auth import ExpiringTokenAuthentication
from user.models import MyUser
from django.core.cache import caches


class GetHasAnalysisView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        account = request.GET.get('account', '')#获取id
        user = MyUser.objects.filter(user__username=account).first()#用户信息
        if user.user_role == 'student':#对于学生和教师处理不同
            select_courses = Course.objects.filter(selectcourse__student__user__username=account,
                                                   course_analysis_zip_data=True)
        else:
            select_courses = Course.objects.filter(course_teacher__user__username=account,
                                                   course_analysis_zip_data=True)
        data = []
        for course in select_courses:
            data.append({'course_name': course.course_name, 'course_id': course.course_id,
                         'course_teacher': course.course_teacher.true_name,
                         'course_year': course.course_year, 'if_analysis': True})
        res = {'code': 200, 'message': '查询成果', 'data': data}
        return JsonResponse(res)#返回数据


class GetKnowledgeCommit(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url=request.get_full_path()
        cache=caches['default']#获取缓存
        data=cache.get(url,{})
        if data!={}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)#存在就返回
        account = request.GET.get('account', '')#获取用户id
        course_id = request.GET.get('course_id', '')#获取学生id
        user = MyUser.objects.filter(user__username=account).first()
        if course_id == '':
            course = Course.objects.filter(selectcourse__student__user__username=account).first()#获取数据第一个数据
        else:
            course = Course.objects.get(course_id=course_id)#有id获取课程id数据
        dir_path = get_dir_path(course)
        file_name = "知识点分析.json"
        commit_data = get_knowledge_data(dir_path, file_name, user.user_number)#读取数据
        res_data = change_commit_data(commit_data, user.user_number)#转化位json
        res_data['course_id']=course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url,res_data)#设置缓存
        return JsonResponse(res)


class GetKnowledgeFirstAccept(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if course_id == '':
            course = Course.objects.filter(selectcourse__student__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "知识点分析.json"
        commit_data = get_knowledge_data(dir_path, file_name, user.user_number)
        res_data = change_first_accept_data(commit_data, user.user_number)
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url,res_data)
        return JsonResponse(res)


class GetKnowledgePass(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if course_id == '':
            course = Course.objects.filter(selectcourse__student__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "知识点分析.json"
        commit_data = get_knowledge_data(dir_path, file_name, user.user_number)
        res_data = change_pass(commit_data, user.user_number)
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)


class GetKnowledgeReturnInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if course_id == '':
            course = Course.objects.filter(selectcourse__student__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "提交返回分析.json"
        commit_data = get_knowledge_data(dir_path, file_name, user.user_number, 'count')
        res_data = change_return_data(commit_data, user.user_number)
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)


class GetLevelAcceptInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if course_id == '':
            course = Course.objects.filter(selectcourse__student__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "难度等级分析.json"
        commit_data = get_knowledge_data(dir_path, file_name, user.user_number, 'mean')
        res_data = change_level_data(commit_data, user.user_number, 'first_accept', 'if_pass')
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        res_data['course_id'] = course.course_id
        cache.set(url, res_data)
        return JsonResponse(res)


class GetLevelCommitInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if course_id == '':
            course = Course.objects.filter(selectcourse__student__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "难度等级分析.json"
        commit_data = get_knowledge_data(dir_path, file_name, user.user_number, 'mean')
        res_data = change_level_data(commit_data, user.user_number, 'commit_count', 'accept_use')
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}

        return JsonResponse(res)


class GetLevelCodeInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if course_id == '':
            course = Course.objects.filter(selectcourse__student__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "难度等级分析.json"
        commit_data = get_knowledge_data(dir_path, file_name, user.user_number, 'mean')
        res_data = change_level_data(commit_data, user.user_number, 'code_line', 'circle_complex')
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)


class GetQuestionTypeInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if course_id == '':
            course = Course.objects.filter(selectcourse__student__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "题目类型分析.json"
        res_data = get_type_data(dir_path, file_name, user.user_number)
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)


class GetStudentDashboardInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if course_id == '':
            course = Course.objects.filter(selectcourse__student__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "用户胜任力分析.json"
        res_data = get_ability_data(dir_path, file_name, user.user_number)
        file_names = ['知识点分析.json', '难度等级分析.json', '题目类型分析.json']
        data2 = get_another_data(dir_path, file_names, user.user_number)
        res_data['another_data'] = data2
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)


class GetStudentStartCommit(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            return JsonResponse(data)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if user.user_role != 'teacher':
            res = {'code': 60404, 'message': '您不是教师没有权限'}
            return JsonResponse(res)
        if course_id == '':
            course = Course.objects.filter(course_teacher__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "作业开始时间分析.json"
        res_data = get_start_data(dir_path, file_name)
        #res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data,'course_id':course.course_id}
        cache.set(url, res)
        return JsonResponse(res)


class GetReturnSumInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if user.user_role != 'teacher':
            res = {'code': 60404, 'message': '您不是教师没有权限'}
            return JsonResponse(res)
        if course_id == '':
            course = Course.objects.filter(course_teacher__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "提交返回分析.json"
        res_data = get_return_sum(dir_path, file_name)
        res = {'code': 200, 'message': '查询成果', 'data': res_data,'course_id':course.course_id}
        return JsonResponse(res)


class GetAbilitySumInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if user.user_role != 'teacher':
            res = {'code': 60404, 'message': '您不是教师没有权限'}
            return JsonResponse(res)
        if course_id == '':
            course = Course.objects.filter(course_teacher__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "用户胜任力分析.json"
        res_data = get_ability_sum_data(dir_path, file_name)
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)

class GetKnowledgeSummaryInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if user.user_role != 'teacher':
            res = {'code': 60404, 'message': '您不是教师没有权限'}
            return JsonResponse(res)
        if course_id == '':
            course = Course.objects.filter(course_teacher__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "知识点分析.json"
        res_data = get_summary_know_data(dir_path, file_name)
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)

class GetLevelSummaryInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if user.user_role != 'teacher':
            res = {'code': 60404, 'message': '您不是教师没有权限'}
            return JsonResponse(res)
        if course_id == '':
            course = Course.objects.filter(course_teacher__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "难度等级分析.json"
        res_data = get_summary_level_data(dir_path, file_name)
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)

class GetTypeSummaryInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if user.user_role != 'teacher':
            res = {'code': 60404, 'message': '您不是教师没有权限'}
            return JsonResponse(res)
        if course_id == '':
            course = Course.objects.filter(course_teacher__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.get(course_id=course_id)
        dir_path = get_dir_path(course)
        file_name = "题目类型分析.json"
        res_data = get_summary_type_data(dir_path, file_name)
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)

class GetTeacherDashboardInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if user.user_role != 'teacher':
            res = {'code': 60404, 'message': '您不是教师没有权限'}
            return JsonResponse(res)
        if course_id == '':
            course = Course.objects.filter(course_teacher__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.filter(course_id=course_id).first()
        if course==None:
            res = {'code': 60404, 'message': '请先进行课程分析'}
            return JsonResponse(res)
        dir_path = get_dir_path(course)
        res_data={}
        file_name = "提交返回分析.json"
        res_data['option1'] = get_return_sum(dir_path, file_name)
        file_name = "作业开始时间分析.json"
        res_data['option2'] = get_start_data(dir_path, file_name)
        file_name = "难度等级分析.json"
        res_data['option3'] = get_summary_level_data(dir_path, file_name)
        file_name = "知识点分析.json"
        res_data['option4'] = get_summary_know_data(dir_path, file_name)
        file_name = "题目类型分析.json"
        res_data['option5'] = get_summary_type_data(dir_path, file_name)
        res_data['course_id'] = course.course_id
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)

class GetTeacherCompareInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        url = request.get_full_path()
        cache = caches['default']
        data = cache.get(url, {})
        if data != {}:
            res = {'code': 200, 'message': '查询成果', 'data': data}
            return JsonResponse(res)
        account = request.GET.get('account', '')
        course_id1 = request.GET.get('course_id1', '')
        course_id2 = request.GET.get('course_id2', '')
        user = MyUser.objects.filter(user__username=account).first()
        if user.user_role != 'teacher':
            res = {'code': 60404, 'message': '您不是教师没有权限'}
            return JsonResponse(res)
        course_list= Course.objects.filter(course_teacher__user__username=account,
                                           course_analysis_zip_data=True)
        if course_list.count()<2:
            res = {'code': 60404, 'message': '完成分析课程不足，请先进行课程分析'}
            return JsonResponse(res)
        if course_id1 != "":
            course1 = Course.objects.filter(course_id=course_id1).first()
            if course1==None:
                res = {'code': 60404, 'message': '输入错误课程，重新输入'}
                return JsonResponse(res)
        else:
            course1=course_list[0]
        if course_id2 != "":
            course2 = Course.objects.filter(course_id=course_id2).first()
            if course2 ==None:
                res = {'code': 60404, 'message': '输入错误课程，重新输入'}
                return JsonResponse(res)
        else:
            course2 = course_list.exclude(course_id=course1.course_id).first()

        dir_path1 = get_dir_path(course1)
        dir_path2 = get_dir_path(course2)
        res_data={}
        file_name = "提交返回分析.json"
        res_data['option1'] = get_return_sum(dir_path1, file_name)
        file_name = "提交返回分析.json"
        res_data['option2'] = get_return_sum(dir_path2, file_name)
        file_name = "难度等级分析.json"
        res_data['option3'] = get_compare_level_data(dir_path1,dir_path2,file_name)
        file_name = "题目类型分析.json"
        res_data['option4'] = get_copmare_type_data(dir_path1, dir_path2,file_name)
        res_data['course1_id'] = course1.course_id
        res_data['course2_id'] = course2.course_id
        res_data['course1_name'] = course1.course_name
        res_data['course2_name'] = course2.course_name
        res = {'code': 200, 'message': '查询成果', 'data': res_data}
        cache.set(url, res_data)
        return JsonResponse(res)

class GetHomeworkCommitInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        account = request.GET.get('account', '')
        course_id = request.GET.get('course_id', '')
        user = MyUser.objects.filter(user__username=account).first()
        if user.user_role != 'teacher':
            res = {'code': 60404, 'message': '您不是教师没有权限'}
            return JsonResponse(res)
        if course_id == '':
            course = Course.objects.filter(course_teacher__user__username=account,
                                           course_analysis_zip_data=True).first()
        else:
            course = Course.objects.filter(course_id=course_id).first()

        dir_path = get_dir_path(course)
        file_name = "单个作业提交分析.json"
        res_data = get_homework_sum(dir_path, file_name)
        res = {'code': 200, 'message': '查询成果', 'data': res_data,'course_id':course.course_id}
        return JsonResponse(res)