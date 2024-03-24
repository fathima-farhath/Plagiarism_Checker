from django.shortcuts import render
from . models import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from datetime import datetime
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

@login_required(login_url='login')   
def edit_workspace(request,workspace_id):
    workspace = WorkSpace.objects.get(id=workspace_id)
    if request.method == "POST":
        workspace.name = request.POST.get('name')
        workspace.stream = request.POST.get('stream')
        workspace.details = request.POST.get('detail')
        workspace.save()
        messages.success(request, 'worspace details updated successfully!')
        return redirect('teacher')  # Replace 'teacher' with the appropriate URL name
    else:
        return render(request, 'class/edit_class.html', {'workspace': workspace}) 


@login_required(login_url='login')
def add_assignment(request, workspace_id):
    workspace = WorkSpace.objects.get(id=workspace_id)
    
    if request.method == 'POST':
        title = request.POST['title']
        instructions = request.POST['instructions']
        pdf = request.FILES['pdf']
        due_date = request.POST['due-date']
        points=request.POST['points']
        
        # Fetch the current logged-in teacher
        teacher = request.user.teachers  
        
        # Create the assignment and link it to the teacher and workspace
        assignment=Assignment.objects.create(workspace=workspace, teacher=teacher, title=title, instructions=instructions, pdf=pdf, points=points, due_date=due_date)
        assignment.save()
        return redirect('open_workspace', workspace_id=workspace_id)
    
    return render(request, 'class/add_assignment.html')

def open_workspace(request, workspace_id):
    single_workspace = WorkSpace.objects.filter(id=workspace_id)
    single_workis = WorkSpace.objects.get(id=workspace_id)
    assignments = Assignment.objects.filter(workspace=single_workis)
    # assignments = single_workspace.assignments.all()
    return render(request,'class/single.html',{'single_workspace':single_workspace,'single_works':single_workis,'assgnmt':assignments})

# def add_assignment(request):
#     return render(request,'class/add_assignment.html')

# def open_workspace(request, workspace_id):
#     workspace = WorkSpace.objects.get(id=workspace_id)
#     assignments = workspace.assignments.all()
#     return render(request, 'workspace.html', {'workspace': workspace, 'assignments': assignments})

def student(request):
    return render(request,'dashboard/student/student.html')
    
def class_base(request):
    return render(request,'class/base.html')


def join(request):
    return render(request,'class/single.html')


def index(request):
    return render(request,'index.html')

def base(request):
    return render(request,'base/base.html')



def send_mail(request):
    return render(request,'dashboard/teacher/send_mail.html')

def recieve_mail(request):
    return render(request,'dashboard/student/email.html')

  
def people(request):
    return render(request,'class/people.html')