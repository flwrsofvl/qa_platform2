from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Question, Answer, Tag

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(max_length=100, required=False, help_text="Введите теги через запятую")

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    pass
