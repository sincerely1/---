import json
import os
import shutil
import zipfile
from io import BytesIO

from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.views.generic.base import View
from django_q.tasks import Chain, async_task

from course_data_analysis.myanalysis import get_level_analysis,get_knowledge_analysis,get_user_ability_analysis,\
    get_one_question_analysis,get_question_type_analysis,get_question_return_analysis,get_question_start_time_analysis
from user.auth import ExpiringTokenAuthentication
from user.models import MyUser
from zip_load.del_courese_info import delete_course_data
from zip_load.load_zip_data import load_zip_data
from zip_load.reset_info import reset_course_info
from zip_load.upload_course_info import upload_course_data
from .models import Course, SelectCourse


class GetCourses(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        account = request.GET.get('account', '')
        courses = Course.objects.filter(course_teacher__user__username=account)
        data = []
        for course in courses:
            data.append({'course_name': course.course_name, 'course_id': course.course_id,
                         'course_teacher': course.course_teacher.true_name, 'course_year': course.course_year})
        res = {'code': 200, 'message': '查询成果', 'data': data}
        return JsonResponse(res)


class GetSelectCourse(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        account = request.GET.get('account', '')
        teacher_name = request.GET.get('teacher_name', '')
        select_courses = Course.objects.filter(selectcourse__student__user__username=account)
        if teacher_name != "":
            select_courses = select_courses.objects.filter(course_teacher=teacher_name)
        data = []
        for course in select_courses:
            data.append({'course_name': course.course_name, 'course_id': course.course_id,
                         'course_teacher': course.course_teacher.true_name,
                         'course_year': course.course_year})
        res = {'code': 200, 'message': '查询成果', 'data': data}
        return JsonResponse(res)


class AddCourseView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        post_body = request.body
        data = json.loads(post_body)
        account = data['teacher_account']
        course_name = data['course_name']
        course_id = data['course_id']
        course_year = data['course_year']
        teacher = MyUser.objects.filter(user__username=account).first()
        if teacher == None:
            res = {'code': 500404, 'message': '教师不存在'}
        else:
            if teacher.user_role == 'teacher':
                courses = Course.objects.filter(course_id=course_id, course_year=course_year,
                                                course_teacher__user__username=account).first()
                if courses:
                    res = {'code': 600210, 'message': '课程已存在'}
                else:
                    course = Course.objects.create(course_name=course_name, course_id=course_id,
                                                   course_year=course_year, course_teacher=teacher)
                    course.save()
                    res = {'code': 200, 'message': '创建成功',
                           'data': {'course_name': course_name, 'course_id': course_id, 'course_year': course_year,
                                    'course_teacher': teacher.true_name}}
            else:
                res = {'code': 500403, 'message': '您不是教师，没权限创建课程'}
        return JsonResponse(res)


class DelCourseView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        post_body = request.body
        data = json.loads(post_body)
        account = data['teacher_account']
        course_id = data['course_id']
        teacher = MyUser.objects.filter(user__username=account).first()
        if teacher == None:
            res = {'code': 500404, 'message': '教师不存在'}
        else:
            if teacher.user_role == 'teacher':
                courses = Course.objects.filter(course_id=course_id, course_teacher__user__username=account).first()
                if courses:
                    courses.delete()
                    res = {'code': 200, 'message': '课程已删除'}
                else:
                    res = {'code': 600210, 'message': '课程不存在'}
            else:
                res = {'code': 500403, 'message': '您不是教师，没权限创建课程'}
        return JsonResponse(res)


class DelSelectCourseView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        post_body = request.body
        data = json.loads(post_body)
        account = data['account']
        course_id = data['course_id']
        select = SelectCourse.objects.filter(course__course_id=course_id, student__user__username=account).first()
        if select == None:
            res = {'code': 500403, 'message': '您不是没有选择该课程'}
        else:
            select.delete()
            res = {'code': 200, 'message': '删除成功'}
        return JsonResponse(res)


class AddSelectCourseView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        post_body = request.body
        data = json.loads(post_body)
        account = data['account']
        course_id = data['course_id']
        select = SelectCourse.objects.filter(course__course_id=course_id, student__user__username=account).first()
        if select != None:
            res = {'code': 500403, 'message': '您已经选择了，不要重复选择'}
        else:
            user = MyUser.objects.filter(user__username=account).first()
            the_course = Course.objects.filter(course_id=course_id).first()
            print(user)
            print(the_course)
            if user == None or the_course == None:
                res = {'code': 600403, 'message': '输入错误重新输入'}
            else:
                select_course = SelectCourse.objects.create(course=the_course, student=user)
                select_course.save()
                res = {'code': 200, 'message': '删除成功'}
        return JsonResponse(res)


class GetNotSelectCourseView(View):

    def get(self, request):
        account = request.GET.get('account', '')
        teacher_name = request.GET.get('teacher_name', '')
        not_select_courses = Course.objects.exclude(selectcourse__student__user__username=account)
        if teacher_name != "":
            not_select_courses = not_select_courses.objects.filter(course_teacher=teacher_name)

        data = []
        for course in not_select_courses:
            data.append({'course_name': course.course_name, 'course_id': course.course_id,
                         'course_teacher': course.course_teacher.true_name,
                         'course_year': course.course_year})
        res = {'code': 200, 'message': '查询成果', 'data': data}
        return JsonResponse(res)


class DownloadDemo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        # 服务器上存放文件的路径
        file_path = "./zip_data/demo/demo.zip"
        try:
            r = StreamingHttpResponse(readFile(file_path))
            r["content_type"] = "application/zip"
            r["Content-Disposition"] = "attachment;demo.zip"
            return r
        except Exception:
            res = {'code': 600403, 'message': '输入错误重新输入'}
            print(res)
            return JsonResponse(res)


def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


class GetUplodInfo(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        account = request.GET.get('account', '')
        courses = Course.objects.filter(course_teacher__user__username=account)
        data = []
        for course in courses:
            data.append({'course_name': course.course_name, 'course_id': course.course_id,
                         'course_teacher': course.course_teacher.true_name, 'course_year': course.course_year,
                         'if_upload': course.course_zip_data, 'if_analysis': course.course_analysis_zip_data})
        res = {'code': 200, 'message': '查询成果', 'data': data}
        return JsonResponse(res)


def save_zip(file_name, dir_path, zip_file):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'wb') as f:
        for chunk in zip_file.chunks():
            f.write(chunk)


def get_dir_path(course):
    dir_name = str(course.course_id) + '_' + str(course.course_year) + "_" + str(course.course_teacher.user_number)
    data_path = './zip_data'
    dir_path = os.path.join(data_path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path


class UploadFileView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        zip_file = request.FILES.get('file')
        course_id = request.POST.get('course_id')
        course = Course.objects.filter(course_id=course_id).first()
        if course.course_zip_data == True:
            res = {'code': 60405, 'message': '存在数据，需要先删除'}
            return JsonResponse(res)
        dir_path = get_dir_path(course)
        save_zip(course.course_name + ".zip", dir_path, zip_file)
        chain = Chain(cached=True)
        chain.append(load_zip_data, course.course_id, course.course_year, course.course_teacher.user_number,
                     course.course_name + '.zip')
        chain.append(upload_course_data, course.course_id, course.course_year, course.course_teacher.user_number,
                     course.course_name)
        chain.append(reset_course_info, course.course_id, course.course_year, course.course_teacher.user_number,
                     course.course_name)
        chain.append(set_zip_data, course_id,True)
        chain.run()
        res = {'code': 200, 'message': '正在上传数据'}
        return JsonResponse(res)


def set_zip_data(course_id,boll_data):
    course = Course.objects.filter(course_id=course_id).first()
    course.course_zip_data = boll_data
    course.save()


def delete_zip_data(zip_path):
    shutil.rmtree(zip_path)
    os.mkdir(zip_path)


class AnalysisView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        post_body = request.body
        data = json.loads(post_body)
        account = data['account']
        course_id = data['course_id']
        user_info = MyUser.objects.filter(user__username=account).first()
        course = Course.objects.filter(course_id=course_id).first()
        if course.course_teacher.user_number != user_info.user_number:
            res = {'code': 60404, 'message': '没有权限分析该课程信息'}
            return JsonResponse(res)
        async_task(get_one_question_analysis, course.course_id, course.course_year, course.course_teacher.user_number)
        async_task(get_question_return_analysis, course.course_id, course.course_year, course.course_teacher.user_number)
        async_task(get_question_type_analysis, course.course_id, course.course_year, course.course_teacher.user_number)
        async_task(get_user_ability_analysis, course.course_id, course.course_year, course.course_teacher.user_number)
        async_task(get_level_analysis, course.course_id, course.course_year, course.course_teacher.user_number)
        async_task(get_knowledge_analysis, course.course_id, course.course_year, course.course_teacher.user_number)
        async_task(get_question_start_time_analysis, course.course_id, course.course_year, course.course_teacher.user_number)
        course.course_analysis_zip_data = True
        course.save()
        res = {'code': 200, 'message': '正在分析课程数据'}
        return JsonResponse(res)



class DeleteDataView(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        post_body = request.body
        data = json.loads(post_body)
        account = data['account']
        course_id = data['course_id']
        user_info = MyUser.objects.filter(user__username=account).first()
        course = Course.objects.filter(course_id=course_id).first()
        if course.course_teacher.user_number != user_info.user_number:
            res = {'code': 60404, 'message': '没有权限删除该课程数据'}
            return JsonResponse(res)
        dir_path = get_dir_path(course)
        chain = Chain(cached=True)
        chain.append(delete_zip_data,dir_path)
        chain.append(delete_course_data, str(course_id))
        chain.append(set_zip_data, course_id,False)
        chain.run()
        # 还需要删除各个table的数据
        course.save()
        res = {'code': 200, 'message': '正在删除数据'}
        return JsonResponse(res)


class ExportAnalysisData(View):
    authentication_classes = (ExpiringTokenAuthentication,)

    def get(self, request):
        account = request.GET.get('account')
        course_id = request.GET.get('course_id')
        user_info = MyUser.objects.filter(user__username=account).first()
        course = Course.objects.filter(course_id=course_id).first()
        if course.course_teacher.user_number != user_info.user_number:
            res = {'code': 60404, 'message': '没有权限导出该课程数据'}
            return JsonResponse(res)
        try:
            startdir = "./analysis_data/1_2018_1"
            buffer = BytesIO()  # 这里是内存，如果是文件名字就是文件了
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)as z:  # 参数一：文件夹名
                for dirpath, dirnames, filenames in os.walk(startdir):
                    fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
                    fpath = fpath and fpath + os.sep or ''
                    for filename in filenames:
                        z.write(os.path.join(dirpath, filename), fpath + filename)
            buffer.seek(0)
            r = StreamingHttpResponse(buffer)
            r["content_type"] = "application/zip"
            r["Content-Disposition"] = "attachment;analysis_result.zip"
            return r
        except Exception:
            res = {'code': 600403, 'message': '输入错误重新输入'}
            print(res)
            return JsonResponse(res)
