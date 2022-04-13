from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect

from BGame.auth_app.forms import EditProfileForm
from BGame.auth_app.models import BGameUser, Profile


class ProfileInLineAdmin(admin.StackedInline):
    model = Profile


class UserAdmin(BaseUserAdmin):
    model = BGameUser

    form = EditProfileForm
    inlines = (ProfileInLineAdmin,)
    list_display = ('username', 'is_superuser', 'is_staff')
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'email')}),

        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups')}),

    )
    fieldsets = (
        (None, {'fields': ('username', 'email')}),

        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups')}),

    )

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/auth_app/bgameuser/')


admin.site.register(BGameUser, UserAdmin)
