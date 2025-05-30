from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from google import genai#Gemini
from django.http import JsonResponse
import google.generativeai as genai  
from .models import *
import markdown
from django.db import models
from django.db.models import Q
from .main import *#вызов нейросети


def study(request):#страница обучения(выбор ИИ или курсы)
    return render(request,'study.html')


@login_required
def ai_teacher(request):#ИИ учитель
    chat_history = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
    return render(request, 'ai-teacher.html', {'chat_history': chat_history})



#ключ
#поменять gpt на gemini
GEMINI_API_KEY = "AIzaSyCaqoqiQsfp_CiDAMB_FXcMCBmdoDmYWpA"
genai.configure(api_key=GEMINI_API_KEY)


@csrf_exempt
@login_required
def chat_with_gemini(request):
    #Обраблтка сообщений: запрос к Gemini -  сохранение в БД- возврат ответа
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()#убираем пробелы
        if not user_message:#Если запрос пустой
            return JsonResponse({"error": "Пустой запрос"}, status=400)
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")#модель gemini-1.5-flash
            response = model.generate_content(user_message)
            #print(user_message) отладочный
            bot_response = getattr(response, "text", "Ошибка генерации ответа")
            bot_response_html = markdown.markdown(bot_response)
            ChatMessage.objects.create( #предаем ответ
                user=request.user,
                message=user_message,
                response=bot_response_html
            )

            return JsonResponse({"response": bot_response_html})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
@login_required
def get_chat_history(request):#загружаем историю чата ИИ
    messages = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
    chat_data = [
        {"user": msg.message, "bot": msg.response} for msg in messages
    ]
    return JsonResponse({"chat_history": chat_data})


def all_courses(request): #все курсы
    categories = Category.objects.all()  #все категории
    courses = Courses.objects.all().order_by('-created_at')
    return render(request, 'all_courses.html', {'categories': categories, 'courses': courses})

def category_courses(request, category_id):#курсы по категориям
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all()
    courses = Courses.objects.filter(category=category)  # Фильтруем курсы по категории
    return render(request, 'all_courses.html', {'courses': courses, 'category': category, 'categories': categories,})

def course_detail(request, course_id):#страница курсы
    course = Courses.objects.get(id=course_id)#id курса
    comments = Comments.objects.filter(course=course).order_by('-created_at')
    if request.method == 'POST':#это коментарии
        text = request.POST.get('text')
        if text.strip():  #Комментарий не должен быть пустым
            Comments.objects.create(user=request.user, course=course, text=text)
        return redirect('course_detail', course_id=course_id)

    return render(request, 'course_detail.html', {'course': course, 'comments': comments})

def about_us(request):#о нас
    return render(request, 'about_us.html')

def news(request):#новости
    news_list = News.objects.all().order_by('-created_at')  
    return render(request, 'news.html', {'news_list': news_list})


@login_required
def mood_text(request):#определение настроения текста
    chat_history = TextClassificationHistory.objects.filter(user=request.user).order_by("-id")
    
    return render(request, "mood_text.html", {"chat_history": chat_history})

@login_required
def mood_text_chat(request):
    if request.method == "POST":#запрос
        user_message = request.POST.get("message", "").strip()
        if user_message:
            # Классифицируем текст
            ai_response = classify_text(user_message)
            print(f"Ответ ИИ: {ai_response}")  # Проверяем, что пришло
            classification, confidence = ai_response.split("(уверенность: ")

            confidence = float(confidence.rstrip(")"))

            # Сохраняем в БД
            TextClassificationHistory.objects.create(
                user=request.user,
                message=user_message,
                classification=classification.strip(),
                confidence=confidence
            )

        # Перенаправление на GET запрос, чтобы избежать повторной отправки формы при обновлении страницы
        return redirect("mood_text_chat")  

    # Получаем историю сообщений из БД
    chat_history = TextClassificationHistory.objects.filter(user=request.user).order_by("-id")
    
    return render(request, "mood_text.html", {"chat_history": chat_history})

@login_required
def test_in_course(request, course_id):#тест курса
    course = get_object_or_404(Courses, id=course_id)
    tests = Test.objects.filter(course=course)#Определяем тест какого курса нам нужен
    score = None
    results = []

    # Проверяем, проходил ли пользователь тест
    completed_tests = CompletedTest.objects.filter(user=request.user, test__in=tests)#выполнение теста
    completed_tests_ids = completed_tests.values_list('test_id', flat=True)

    if request.method == 'POST' and not completed_tests:#Пользователь отправил запрос(ответы)
        correct_answers = 0#правильные ответы
        total_questions = sum(test.questions.count() for test in tests)

        for test in tests:
            for question in test.questions.all():
                selected_answer_id = request.POST.get(f'question_{question.id}')
                selected_answer = Answer.objects.filter(id=selected_answer_id).first()

                # Проверяем правильность ответа
                is_correct = selected_answer and selected_answer.is_correct
                if is_correct:
                    correct_answers += 1

                # Добавляем результат в список
                results.append({
                    'question': question.text,
                    'selected_answer': selected_answer.text if selected_answer else "Не выбрано",
                    'is_correct': is_correct
                })

        score = correct_answers  # Количество правильных ответов

        # Сохраняем в БД, если пользователь не проходил тест ранее
        for test in tests:
            CompletedTest.objects.create(user=request.user, test=test, score=score)

        # Добавляем баллы пользователю
        request.user.score += score
        request.user.save()

        completed_tests_count = CompletedTest.objects.filter(user=request.user, test__in=tests).count()
        if completed_tests_count == tests.count():  #если пользователь прошел все тесты
            request.user.courses_completed += 1  #засчитываем курс
            request.user.save()

    return render(request, 'test.html', {#предаем все переменные(контекст)
        'course': course,
        'tests': tests,
        'score': score,
        'results': results,
        'completed_tests_ids': completed_tests_ids 
    })

def search_user(request):#поиск пользователей
    search = request.GET.get('q')
    users = CustomUser.objects.filter(username__icontains=search) if search else None
    return render(request, 'search_user.html', {'users': users})

@login_required
def messages_view(request, chat_id=None):#чаты
    chats = Chat.objects.filter(user1=request.user) | Chat.objects.filter(user2=request.user)
    
    selected_chat = None
    if chat_id:
        selected_chat = get_object_or_404(Chat, id=chat_id)
    
    return render(request, 'message.html', {'chats': chats, 'selected_chat': selected_chat})


@login_required
def start_chat(request, user_id):#начать чат с пользователем
    user = request.user  #получаем текущего пользователя
    other_user = get_object_or_404(CustomUser, id=user_id)  #пользователь с которым создаётся чат

    chat, created = Chat.objects.get_or_create(
        user1=min(user, other_user, key=lambda u: u.id),
        user2=max(user, other_user, key=lambda u: u.id)
    )

    chats = Chat.objects.filter(Q(user1=user) | Q(user2=user))  # user1 и user2 определён

    return render(request, 'message.html', {'chats': chats})

@login_required
def send_message(request, chat_id):#отправка сообщения
    chat = get_object_or_404(Chat, id=chat_id)
    
    if request.method == 'POST':
        message_text = request.POST.get('message_text')
        if message_text:
            #определяем получателя
            receiver = chat.user1 if chat.user2 == request.user else chat.user2  
            
            #создаём сообщение
            Message.objects.create(chat=chat, sender=request.user, receiver=receiver, text=message_text)

    return redirect('message_with_id', chat_id=chat.id)
