from django.contrib import admin
from django.urls import path,include
from . import views
# from django import views

urlpatterns = [
    path('base/base', views.class_base, name='class_base'),
    path('join/',views.join,name='join'),
    path('',views.index,name='index'),
    path('student_dashboard/', views.student, name = 'student'),

    path('add_assignment/<uuid:workspace_id>/', views.add_assignment, name='add_assignment'),
    path('edit_class/<uuid:workspace_id>/', views.edit_workspace,name='edit_class'),

    path('create_class/', views.create_class,name='create_class'),
    path('delete/<uuid:workspace_id>/', views.delete_workspace, name='delete_workspace'),
    path('workspace/<uuid:workspace_id>/', views.open_workspace, name='open_workspace'),
    # path('single/', views.single, name='single'),
    path('send_mail/', views.send_mail, name = 'send_mail'),
    path('recieve_mail/',views.recieve_mail,name='recieve_email'),
    path('teacher_dashboard/',views.teacher, name='teacher'),
    
    path('student_list/',views.people,name='people'),
]