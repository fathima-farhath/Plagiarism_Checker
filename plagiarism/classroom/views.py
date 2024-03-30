from django.shortcuts import render
from . models import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required(login_url='login')
def create_class(request):
    workspaces=WorkSpace.objects.all()
    if request.method=="POST":
        name = request.POST.get('name')
        detail = request.POST.get('detail')
        stream = request.POST.get('stream')
        teacher = request.user.teachers
        workspace = WorkSpace.objects.create(name=name, details=detail, stream=stream, teacher=teacher)
        
        workspace.save()
        messages.success(request,' Classroom Has Been Created !!')
        return  redirect('teacher') 
    else:
        return render(request,'class/create_class.html') 

@login_required(login_url='login')
def teacher(request):
    teacher = request.user.teachers
    workspaces = WorkSpace.objects.filter(teacher=teacher)
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
    # if request.method == "POST":
    #     code = request.POST.get('code')
    #     try:
    #         #workspace = WorkSpace.objects.get(code=code)
    #         # Assuming the user is a student and has a related student profile
    #         user = request.user
    #         if user.is_authenticated and user.is_student:
    #             # Add the student to the workspace
                
    #             print("Student authemticte")
    #             check_code = WorkSpace.objects.get(code = code)
    #             class_room = WorkSpace.objects.get(id=check_code.id)
    #             check = MemberShip.objects.filter(room = class_room)
    #             if check:
    #                 messages.success(request,'You are already a Mwmber')
    #                 return redirect('single', id=check_code.id) 
    #             else:
    #                 member = MemberShip(room = class_room, student = user)
    #                 member.is_join = True
    #                 member.save()
    #                 messages.success(request, 'Successfully joined the workspace!') 
    #                 print('Successfully joined the workspace!')
    #                 return redirect('student')
    #     except WorkSpace.DoesNotExist:
    #         messages.error(request, 'Invalid workspace code. Please try again.')
    #         print("invalid")
    return render(request,'dashboard/student/student.html')


def index(request):
    return render(request,'index.html')

def base(request):
    return render(request,'base/base.html')

def student(request):
    return render(request, 'dashboard/student/student.html')

def send_mail(request):
    return render(request,'dashboard/teacher/send_mail.html')

def recieve_mail(request):
    return render(request,'dashboard/student/email.html')

  
def people(request):
    return render(request,'class/people.html')