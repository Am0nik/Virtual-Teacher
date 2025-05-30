from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()#Вызываем нашу модель чтобы писать не CustomUser, а просто User

class LoginForm(forms.Form):#Форма для входа
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": "form-control-login", "placeholder": "Введите имя"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control-login", "placeholder": "Введите email"}))


class ProfileUpdateForm(forms.ModelForm):#Форма для реадктирования профиля
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя"})
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"})
    )
    age = forms.IntegerField(
        label="Возраст",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Введите возраст"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "age"]



class CustomUserCreationForm(UserCreationForm):#Форма для регистрации
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control-login", "placeholder": "Введите имя"}),
        error_messages={"unique": "Этот логин уже занят"}#Если занять логин, то отпраыляет ошибку
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control-login", "placeholder": "Введите email"}),
        error_messages={"invalid": "Введите корректный email"}#Если email не соответсвует(не рабочий) тоже отправляет ошибку
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control-login", "placeholder": "Введите пароль"}),
        error_messages={#проверка на длинну и сложность пароля
            "password_too_short": "Пароль должен содержать минимум 8 символов",
            "password_too_common": "Пароль слишком простой",
            "password_entirely_numeric": "Пароль не должен состоять только из цифр"
        }
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control-login", "placeholder": "Повторите пароль"}),
        error_messages={"password_mismatch": "Пароли не совпадают"}#Если пароли не совподают
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
