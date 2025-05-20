from django import forms
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