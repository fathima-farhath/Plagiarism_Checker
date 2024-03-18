
from django.urls import path
from . import views
from .views import TeacherRegister, StudentRegister,LoginView,LogoutView
from .views import TeacherDashboard
from .views import StudentDashboard

urlpatterns = [
    path('',views.index,name='index'),
    path('base/', views.base, name='base'),
    
    path('signup_teacher/',TeacherRegister.as_view(),name='signup'),
    path('signup_student/',StudentRegister.as_view(),name='student_register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    
    path('teacher/',TeacherDashboard.as_view(),name='teacher'),
    path('student/',StudentDashboard.as_view(),name='student'),
]