# from django.contrib import admin
# from django.contrib.auth.models import Group
#
# from django.contrib import admin
#
# from django.contrib.auth.models import User, Group
# from .models import Profile
#
#
# class ProfileInline(admin.StackedInline):
#     model = Profile
#
# class UserAdmin(admin.ModelAdmin):
#     model = User
#     fields = ["username"]
#     inlines = [ProfileInline]
#
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", ]


admin.site.register(CustomUser, CustomUserAdmin)
