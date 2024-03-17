from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # path('',views.index,name='index'),
    path('base/', views.base, name='base'),
    # path('signup/', views.signup, name = 'signup'),
    # path('login/', views.login, name = 'login'),
    
    path('student_dashboard/', views.student, name = 'student'),
    path('send_mail/', views.send_mail, name = 'send_mail'),
    path('recieve_mail/',views.recieve_mail,name='recieve_email'),
    path('teacher_dashboard/',views.teacher, name='teacher'),
    
    path('create_class/', views.create_class,name='create_class'),
    path('student_list/',views.people,name='people'),
]