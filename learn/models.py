from django.db import models
from django.contrib.auth import get_user_model
import uuid
from account.models import CustomUser
from ckeditor.fields import RichTextField

User = get_user_model()

class ChatSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):#чат с ИИ
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True) 
    response = models.TextField()
    role = models.CharField(max_length=10, choices=[("user", "User"), ("assistant", "Assistant")])#роли юзер или ИИ(нужно для того чтобы сообщения были с разных сторон экрана)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user or self.session} ({self.role}): {self.message[:50]}"

class Category(models.Model):  #категории
    name = models.CharField(max_length=255, unique=True)  #название категории

    def __str__(self):
        return self.name  #показывает название категории в админке 


class Courses(models.Model):#курс
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Преподаватель")
    title = models.CharField(max_length=255, verbose_name="Название курса")
    description = RichTextField(verbose_name="Описание курса")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", default="Без категории")
    image = models.ImageField(upload_to="course_images/", verbose_name="Изображение")
    video = models.FileField(upload_to="course_videos/", null=True, blank=True, verbose_name="Видео (файл)")
    video_des = models.TextField(verbose_name="Описание к видео", null=True, blank=True)
    video_url = models.URLField(verbose_name="Ссылка на YouTube", null=True, blank=True)
    file = models.FileField(upload_to="course_files/", null=True, blank=True, verbose_name="Файл")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")#для сортировки
    course_it = RichTextField(verbose_name="Сам курс", default="")

    def __str__(self):
        return self.title
    

class News(models.Model):#новости
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = RichTextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    image = models.ImageField(upload_to="news_images/", verbose_name="Изображение", null=True, blank=True)

    def __str__(self):
        return self.title

class TextClassificationHistory(models.Model):#нейросеть по определению насторения
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    classification = models.CharField(max_length=255)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.classification} ({self.confidence:.2f})"



class Test(models.Model):#тест
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="tests")#привязывается к курсу
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"Тест для курса: {self.course.title}"

class Question(models.Model):#вопросы
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")#привязываются к тесту
    text = models.TextField()

    def __str__(self):
        return f"Вопрос: {self.text[:50]}..."

class Answer(models.Model):#ответы
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")#привязываются к вопросам
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Ответ: {self.text} ({'Правильный' if self.is_correct else 'Неправильный'})"
    

class CompletedTest(models.Model):#выполнение теста
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()  #сколько баллов за тест

    class Meta:
        unique_together = ('user', 'test')  #больше 1 раза нельзя проходить тест


class Comments(models.Model):#коментарии
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Автор комментария
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)  # Курс к которому относится комментарий
    text = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.course.title}"


class Chat(models.Model):#чаты
    users = models.ManyToManyField(User)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_as_user1")#собеседник 1
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_as_user2")#собеседник 2
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чат между {self.user1.username} и {self.user2.username}"
    
class Message(models.Model):#сообщения
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")#к какому чату привязываются сообщения
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')#отправитель
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True, default=1)#польучатель
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

