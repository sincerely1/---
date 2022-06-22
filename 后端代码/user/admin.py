from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import MyUser


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_superuser')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'true_name', 'introduction', 'user_number', 'user_role']
