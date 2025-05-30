from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static#для работы с медиа из статических файлов

urlpatterns = [
    path('study/',views.study,name="study"),#страница с вариантами обучения
    path('study/ai-teacher/', views.ai_teacher, name='ai-teacher'),#ИИ учитель
    path('chat/',views.chat_with_gemini, name='chat_with_gemini'),#чат 
    path('chat/history/', views.get_chat_history, name='get_chat_history'),#загрузка истории чата 
    path('all-courses/', views.all_courses, name='all_courses'),#все курсы
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),#страница курса
    path('about-us', views.about_us, name='about-us'),#о нас
    path('news/', views.news, name='news'),#новости
    path('mood-text/', views.mood_text, name='mood-text'),#нейросеть(определение настоения текста)
    path("mood-text/chat/", views.mood_text_chat, name="mood_text_chat"),#чат с нейросетью
    path('test/<int:course_id>/',views.test_in_course,name='test'),#тест
    path('search/',views.search_user,name='search-user'),#поиск пользователей
    path('message/', views.messages_view, name='message'),  # Для страницы всех сообщений
    path('message/<int:chat_id>/', views.messages_view, name='message_with_id'),# Страница со всеми чатами
    path('start_chat/<int:user_id>/', views.start_chat, name='start_chat'),#начать чат с пользователм
    path('message/send/<int:chat_id>/', views.send_message, name='send_message'),#отправить сообщение
    path('courses/category/<int:category_id>/', views.category_courses, name='category_courses'),#курсы по категориям
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#поключение медиа статических файлов
