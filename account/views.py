from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm 
User = get_user_model()#Наша модель, чтобы писать User , а не CustomUser

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():#Если форма валидна(проверяется в forms.py), то идет запись пользовтаеля в БД
            user = form.save()#Сохранение в БД
            #print(user) это был отладочный принт
            login(request, user)  
            messages.success(request, "Регистрация успешна!")
            return redirect("profile") #После регистрации отправляет на страницу профиля
        else:
            messages.error(request, "Ошибка при регистрации. Проверьте данные.") #если форма не валидна
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():#если форма валидна(корректна)
            user = form.get_user()
            login(request, user)#вход в систему
            messages.success(request, "Вы вошли в систему!")
            return redirect("profile") 
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

@login_required(login_url="login")#можно зайти только если выполнен вход в систему, а иначе перекидывает на страницу входа
def profile(request):
    return render(request, "profile.html", {"user": request.user})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():#Проверяет форму на корректность 
            form.save()#сохраняет  изменения в БД
            messages.success(request, "Профиль успешно обновлён!")
            return redirect("profile") 
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "edit_profile.html", {"form": form})