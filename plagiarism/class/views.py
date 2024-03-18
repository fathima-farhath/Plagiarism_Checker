from django.shortcuts import render
from . models import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404

# Create your views here.
def create_class(request):
    workspaces=WorkSpace.objects.all()
    if request.method=="POST":
        name = request.POST.get('name')
        detail = request.POST.get('detail')
        stream = request.POST.get('unit')
        workspace=WorkSpace(name=name,details=detail,stream=stream)
        workspace.save()
        messages.success(request,' Classroom Has Been Created !!')
        return  redirect('teacher') 
    else:
        return render(request,'class/create_class.html') 

def teacher(request):
    workspaces = WorkSpace.objects.all()
    if not workspaces:
        messages.success(request,'No workspce exists !!')
    return render(request,'dashboard/teacher/teacher.html',{'workspace': workspaces}) 
    
def delete_workspace(request, workspace_id):
    try:
        workspace = WorkSpace.objects.get(id=workspace_id)
        workspace.delete()
        return redirect('teacher')
    except WorkSpace.DoesNotExist:
        raise Http404("Workspace does not exist")


def open_workspace(request, workspace_id):
    single=workspace = WorkSpace.objects.filter(id=workspace_id)
    return render(request,'class/single.html',{'single_workspace':single})

def class_base(request):
    return render(request,'class/base.html')


def join(request):
    return render(request,'class/single.html')


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
def people(request):
    return render(request,'class/people.html')