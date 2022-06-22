from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    true_name = models.CharField(max_length=20, verbose_name="姓名")
    introduction = models.CharField(max_length=40, verbose_name="介绍", default="I am a normal user")
    user_avatar = models.URLField(verbose_name="用户头像",
                                  default='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif')
    user_number = models.CharField(max_length=20, verbose_name="学号/教师号/管理员编号")
    user_role = models.CharField(max_length=10, choices=(("student", "学生"), ("teacher", "教师"), ("admin", "管理员")),
                                 default="student")

    def __str__(self):
        return self.true_name

    @staticmethod
    def create_user(account, true_name, user_number, user_role, introduction="I am a normal user",
                    user_avatar="'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'",
                    password='ps123456'):
        if not User.objects.filter(username=account).exists():
            new_user = User.objects.create_user(username=account, password=password)
            new_user.save()
            new_my_user = MyUser.objects.create(user=new_user, true_name=true_name, introduction=introduction,
                                                user_avatar=user_avatar,
                                                user_number=user_number, user_role=user_role)
            new_my_user.save()
            return new_my_user
        else:
            return None
