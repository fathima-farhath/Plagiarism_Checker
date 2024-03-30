from django.urls import path
from . import views
# from django import views

urlpatterns = [
   # path('', views.plagiarism_checker, name = 'plagiarism_checker'),
    path('',views.plagiarism_checker2, name = 'plagiarism_checker2')
]
