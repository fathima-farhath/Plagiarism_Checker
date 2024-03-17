from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('base/', views.base, name='base'),
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name = 'login'),
]