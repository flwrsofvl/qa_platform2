from django.urls import path
from qa import views 

app_name = 'qa'

urlpatterns = [
    path('', views.home, name='home'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
    path('answer/<int:answer_id>/rate/<int:rating>/', views.rate_answer, name='rate_answer'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
