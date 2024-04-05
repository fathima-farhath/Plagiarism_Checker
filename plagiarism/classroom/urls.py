
from django.urls import path
from . import views

# from django import views

urlpatterns = [
    path('base/base', views.class_base, name='class_base'),
    path('join/',views.join,name='join'),
    path('',views.index,name='index'),

    path('add_assignment/<uuid:workspace_id>/', views.add_assignment, name='add_assignment'),
    path('delete/<uuid:assignment_id>/',views.delete_assignment,name='delete_assignment'),
    path('update/<uuid:assignment_id>/',views.update_assignment,name='update_assignment'),

    path('create_class/', views.create_class,name='create_class'),
    path('edit_class/<uuid:workspace_id>/', views.edit_workspace,name='edit_class'),
    path('delete/<uuid:workspace_id>/', views.delete_workspace, name='delete_workspace'),
    path('workspace/<uuid:workspace_id>/', views.open_workspace, name='open_workspace'),
    # path('single/', views.single, name='single'),
    path('send_mail/', views.send_mail, name = 'send_mail'),
    path('recieve_mail/',views.recieve_mail,name='recieve_email'),

    path('student_dashboard/', views.student, name = 'student'),
    path('teacher_dashboard/',views.teacher, name='teacher'),
    path('join_workspace/',views.join,name='join'),
    path('submit_work/<uuid:assignment_id>/',views.submit_assignment,name='submit_assignment'),
    path('update_work/<uuid:assignment_id>/',views.update_sub,name='update_sub'),
    path('view_sub/<uuid:assignment_id>/',views.view_sub,name='view_sub'),
    path('student_list/<uuid:workspace_id>/',views.people,name='people'),

    path('grade/<uuid:submission_id>/',views.automatic_grading,name='automatic_grading'),
    path('edit_grade/<uuid:submission_id>/', views.edit_grade, name='edit_grade'),

]