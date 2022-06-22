from django.db import models

from user.models import MyUser


# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=20, verbose_name="课程名称")
    course_id = models.CharField(max_length=20, verbose_name='课程编号')
    course_teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course_year = models.IntegerField(verbose_name='课程年份')
    course_introduction = models.CharField(max_length=40, verbose_name='课程介绍', default='一门简单易学的课程')
    course_zip_data = models.BooleanField(default=False, verbose_name='课程数据')
    course_analysis_zip_data=models.BooleanField(default=False,verbose_name='分析数据')

    class Meta:
        ordering = ['course_id']

    def __str__(self):
        return self.course_name


class SelectCourse(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    @staticmethod
    def create_select_info(course_id, student_id):
        course = Course.objects.get(course_id=course_id)
        student = MyUser.objects.get(user_numbser=student_id)
        select_course = SelectCourse.objects.get_or_create(course=course, student=student)
        select_course.save()
        return select_course
