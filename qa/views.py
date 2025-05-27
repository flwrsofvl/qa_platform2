from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Question, Answer, Tag
from .forms import QuestionForm, AnswerForm, CustomUserCreationForm, CustomAuthenticationForm

def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'qa/home.html', {'questions': questions})

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
            return redirect('question_detail', question_id=question.id)
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
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    question.tags.add(tag)
            
            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm()
    
    return render(request, 'qa/ask_question.html', {'form': form})

@login_required
def rate_answer(request, answer_id, rating):
    answer = get_object_or_404(Answer, pk=answer_id)
    if 1 <= rating <= 5:
        answer.rating = rating
        answer.save()
    return redirect('question_detail', question_id=answer.question.id)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'qa/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'qa/login.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')
