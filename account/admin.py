from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "age", "courses_completed", "date_joined", "is_staff")
    search_fields = ("username", "email")
    ordering = ("date_joined",)
    
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Персональная информация", {"fields": ("age", "courses_completed","score","role")}),#Что будет отображаться во вкладке важная информация
        ("Разрешения", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login",)}), 
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
#Нашу модель CustomUser мы регистрируем в алмин панели, чтобы контролировать пользователей