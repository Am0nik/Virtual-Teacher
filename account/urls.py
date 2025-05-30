from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", register, name="register"),#url на страницу регистрации
    path("login/", user_login, name="login"),#url на страницу входа
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),#выход из аккаунта
    path("profile/", profile, name="profile"),#url на страницу профиля
    path("edit-profile/", edit_profile, name="edit"),#url на станицу редактирования профиля
]
