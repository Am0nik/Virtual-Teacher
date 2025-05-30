from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)#почта
    age = models.PositiveIntegerField(null=True, blank=True)#возраст(не обязательно)
    courses_completed = models.PositiveIntegerField(default=0)#кол-во выполненных курсов(по умолчанию 0)
    date_joined = models.DateTimeField(auto_now_add=True)#дата регистрации
    score = models.PositiveIntegerField(default=0)#очки(по умолчанию 0)
    role = models.CharField(max_length=20, default='Участник')#роль(зависит от очков и по умолчанию "Участник")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_role(self):
        #Роль зависит от очков. Это создано для мотивации :)
        if self.is_superuser:#Если админ, то роль админ
            return "Админ"
        elif self.score >= 1000:#Если больше или равно 1000 очков, то роль робот
            return "Робот"
        elif self.score > 200:#Если больше 200 очков, то роль сверхразум
            return "Сверхразум"
        elif self.score > 100:#если больше 100 очков, то роль отличник
            return "Отличник"
        elif self.score > 10:#если больше 10 очков, то роль хорошист
            return "Хорошист"
        return "Участник"

    def save(self, *args, **kwargs):
        #Автоматически обновляет роль перед сохранением
        self.role = self.get_role()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role()})"