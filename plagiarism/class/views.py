from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def base(request):
    return render(request,'base/base.html')

def signup(request):
    return render(request,'register/signup.html')

def login(request):
    return render(request,'register/login.html')

def student(request):
    return render(request, 'dashboard/student/student.html')

def send_mail(request):
    return render(request,'dashboard/teacher/send_mail.html')

def recieve_mail(request):
    return render(request,'dashboard/student/email.html')

def teacher(request):
    return render(request,'dashboard/teacher/teacher.html') 

def create_class(request):
    return render(request,'class/create_class.html') 
  
def people(request):
    return render(request,'class/people.html')