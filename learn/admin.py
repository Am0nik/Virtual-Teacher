from django.contrib import admin
from .models import ChatMessage, ChatSession, Courses, News,TextClassificationHistory, Answer, Question, Test, Comments, Chat, Message, Category,CompletedTest

#регистрация моделей
@admin.register(ChatMessage)
@admin.register(ChatSession)
@admin.register(Courses)
@admin.register(News)
@admin.register(TextClassificationHistory)
class DefaultAdmin(admin.ModelAdmin):
    pass

# Inline-классы (НЕ РЕГИСТРИРУЕМ)
class AnswerInline(admin.TabularInline):  
    model = Answer  
    extra = 3  # минимум 3 варианта ответа

class QuestionInline(admin.TabularInline):  
    model = Question  
    extra = 3  # минимум 3 вопроса

# Админ-панель для тестов
@admin.register(Test)  
class TestAdmin(admin.ModelAdmin):  
    list_display = ('title', 'course')  
    inlines = [QuestionInline]  

# Админ-панель для вопросов
@admin.register(Question)  
class QuestionAdmin(admin.ModelAdmin):  
    list_display = ('text', 'test')  
    inlines = [AnswerInline]  

# Админ-панель для ответов
@admin.register(Answer)  
class AnswerAdmin(admin.ModelAdmin):  
    list_display = ('text', 'question', 'is_correct')  

#Коментарии
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at', 'text')  # Отображаемые поля(в админке)
    search_fields = ('user__username', 'course__title', 'text')  # Поиск по нику,названию курса или тексту
    list_filter = ('course', 'created_at')  #фильтр по дате

#сообщения
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'created_at')
    search_fields = ('user1__username', 'user2__username')
    ordering = ('-created_at',)

#чаты(сообщения)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'text', 'created_at') 

#категории
admin.site.register(Category)
#выполнение теста(для откатки на этапе тестировки)
admin.site.register(CompletedTest)