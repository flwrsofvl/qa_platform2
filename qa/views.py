from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout # Добавил logout для ясности
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Question, Answer, Tag
from .forms import QuestionForm, AnswerForm, CustomUserCreationForm, CustomAuthenticationForm
from django.core.paginator import Paginator
from django.utils.text import slugify # ДОБАВЛЕНО: Импорт slugify

def home(request):
    questions = Question.objects.all().order_by('-created_at')

    # Поиск по названию вопроса
    search_query = request.GET.get('q')
    if search_query:
        questions = questions.filter(title__icontains=search_query)

    # Поиск по авторам
    author_query = request.GET.get('author')
    if author_query:
        questions = questions.filter(author__username__icontains=author_query)

    # Фильтрация по тегам
    tag_slug = request.GET.get('tag')
    if tag_slug:
        questions = questions.filter(tags__slug=tag_slug)

    # Пагинация
    paginator = Paginator(questions, 10) # 10 вопросов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем все теги для отображения в фильтре
    all_tags = Tag.objects.all().order_by('name')

    return render(request, 'qa/home.html', {
        'questions': page_obj,
        'page_obj': page_obj,
        'tags': all_tags,
        'current_search_query': search_query if search_query else '',
        'current_author_query': author_query if author_query else '',
        'current_tag_slug': tag_slug if tag_slug else ''
    })

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers.all().order_by('-rating', '-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            # ИЗМЕНЕНО: Добавлено пространство имен 'qa:'
            return redirect('qa:question_detail', question_id=question.id)
    else:
        form = AnswerForm()

    return render(request, 'qa/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()

            tags = form.cleaned_data['tags'].split(',')
            for tag_name in tags:
                tag_name = tag_name.strip()
                if tag_name: # Убедимся, что имя тега не пустое
                    # Убедимся, что slug не будет пустым
                    if slugify(tag_name):
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        question.tags.add(tag)

            # ИЗМЕНЕНО: Добавлено пространство имен 'qa:'
            return redirect('qa:question_detail', question_id=question.id)
    else:
        form = QuestionForm()

    return render(request, 'qa/ask_question.html', {'form': form})

@login_required
def rate_answer(request, answer_id, rating):
    answer = get_object_or_404(Answer, pk=answer_id)
    if 1 <= rating <= 5:
        answer.rating = rating
        answer.save()
    # ИЗМЕНЕНО: Добавлено пространство имен 'qa:'
    return redirect('qa:question_detail', question_id=answer.question.id)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # ИЗМЕНЕНО: Добавлено пространство имен 'qa:'
            return redirect('qa:home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'qa/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('qa:home')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'qa/login.html', {'form': form})

def logout_view(request):
    logout(request)
    # ИЗМЕНЕНО: Добавлено пространство имен 'qa:'
    return redirect('qa:home')