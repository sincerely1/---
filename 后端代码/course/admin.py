# Register your models here.
from django.contrib import admin

from .models import Course,SelectCourse


# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'course_id', 'course_teacher', 'course_year', 'course_introduction']


@admin.register(SelectCourse)
class SelectCourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'student_name','student_number']

    def student_name(self, obj):
        return obj.student.true_name
    student_name.short_description = '姓名'
    def student_number(self, obj):
        return obj.student.user_number
    student_number.short_description = '学号'
