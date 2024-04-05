from . models import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404
import os
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import joblib
from pprint import PrettyPrinter
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import fitz  # PyMuPDF
import tempfile
from ML_model.views import *
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
        messages.success(request,' workspace Has Been Created !!')
        return  redirect('teacher') 
    else:
        return render(request,'class/create_class.html') 

@login_required(login_url='login')
def teacher(request):
    teacher = request.user.teachers
    workspaces = WorkSpace.objects.filter(teacher=teacher).order_by('-created_at')
    if not workspaces:
        messages.success(request,'No workspce exists !!')
    return render(request,'dashboard/teacher/teacher.html',{'workspace': workspaces}) 


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

def delete_workspace(request, workspace_id):
    print("Hello")
    try:
        workspace = WorkSpace.objects.get(id=workspace_id)
        workspace.delete()
        messages.success(request,'Workspace deleted Successfully')
        return redirect('teacher')
    except WorkSpace.DoesNotExist:
        raise Http404("Workspace does not exist")

@login_required(login_url='login')
def add_assignment(request, workspace_id):
    workspace = WorkSpace.objects.get(id=workspace_id)
    
    if request.method == 'POST':
        title = request.POST['title']
        instructions = request.POST['instructions']
        pdf = request.FILES['pdf']
        due_date = request.POST['due-date']
        points=request.POST['points']
        teacher = request.user.teachers
        # Create the assignment and link it to the teacher and workspace
        assignment=Assignment.objects.create(workspace=workspace, teacher=teacher, title=title, instructions=instructions, pdf=pdf, points=points, due_date=due_date)
        assignment.save()
        return redirect('open_workspace', workspace_id=workspace_id)
    
    return render(request, 'class/add_assignment.html')
 
def delete_assignment(request, assignment_id):
    try:
        assignment=Assignment.objects.get(id=assignment_id)
        if assignment.pdf:
            file_path = os.path.join(settings.MEDIA_ROOT, str(assignment.pdf))
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                raise FileNotFoundError("File does not exists at the path:{}".format(file_path))
        assignment.delete()
        return redirect('open_workspace',workspace_id=assignment.workspace.id)
    except:
        raise Http404("No such assignment exists")

@login_required(login_url='login')   
def update_assignment(request,assignment_id):
    assignment=Assignment.objects.get(id=assignment_id)
    if request.method=='POST':
        assignment.title = request.POST['title']
        assignment.instructions = request.POST['instructions']
        # assignment.pdf = request.FILES['pdf']
        assignment.due_date = request.POST['due-date']
        assignment.points=request.POST['points']
        if 'pdf' in request.FILES:
            assignment.pdf = request.FILES['pdf']
        assignment.save()
        return redirect('open_workspace', workspace_id=assignment.workspace_id)
    else:
        return render(request,'class/update_assignment.html',{'assgnmt':assignment})



@login_required(login_url='login')   
def join(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            workspace = WorkSpace.objects.get(code=code)
            print(workspace)
            student = request.user.students
            print(student)
            # Check if the student is already a member of the workspace
            if not Membership.objects.filter(student=student, workspace=workspace).exists():
                Membership.objects.create(student=student, workspace=workspace)
                messages.success(request,'You have successfully joined the workspace!!')
                return redirect('student')
            else:
                messages.success(request,'You have already joined the Workspace!!')
                return redirect('student')  # Change 'student_dashboard' to the URL name of your student dashboard
        except WorkSpace.DoesNotExist:
            messages.success(request,'The code is invalid.Please enter the correct code!!')
            return redirect('student')
    return redirect('.')

def submit_assignment(request,assignment_id):
    assignment=Assignment.objects.filter(id=assignment_id)
    assignments=Assignment.objects.get(id=assignment_id)
    student = request.user.students

    existing_submission = Submission.objects.filter(assignment=assignments, student=student).exists()

    if request.method == 'POST':
        # If submission already exists, redirect or show an error message
        if existing_submission:
            messages.success(request,' You have already submitted this assignment !!')
            # return HttpResponse("You have already submitted this assignment", status=400)
            return redirect('.')    
        pdf = request.FILES['pdfdoc']
        sub=Submission.objects.create(submitted_file=pdf,assignment=assignments,student=student)
        sub.save()
        messages.success(request,'Submission successful')
        return redirect('.')    
    submissions = Submission.objects.filter(assignment=assignments, student=student)
    return render(request,'class/add_sub.html', {'assignment': assignment, 'submissions': submissions})


def update_sub(request,assignment_id):
    assignment=Assignment.objects.filter(id=assignment_id)
    assignments=Assignment.objects.get(id=assignment_id)
    student = request.user.students
    submissions = Submission.objects.filter(assignment=assignments, student=student)
    if request.method == 'POST':
        sub = Submission.objects.get(assignment=assignments, student=student)
        sub.submitted_file=request.FILES['pdfdoc']
        sub.save()
        messages.success(request,"Submission updated successfully")
    return render(request,'class/update_sub.html',{'assignment': assignment, 'submissions': submissions})



        #messages.success("Plagiarism amount= ",plagiarism_amount)

@login_required(login_url='login')   
def student(request):
    result,is_plagiarized=check(request)
    student = request.user.students
    # Get the workspaces joined by the student
    joined_workspaces = WorkSpace.objects.filter(membership__student=student).order_by('-membership__joining_date')
    if result is not None:
        if is_plagiarized:
            message = f"The document is plagiarized with {result:.2f}% plagiarism."
        else:
            message = "The document is not plagiarized."
    else:
        message = None
    return render(request, 'dashboard/student/student.html', {'joined_workspaces': joined_workspaces,'message': message})  

def people(request,workspace_id):
    workspace = WorkSpace.objects.get(id=workspace_id)
    memberships = Membership.objects.filter(workspace=workspace)
    joined_students_names = [membership.student.name for membership in memberships]
    return render(request,'class/people.html',{'joined_students_names': joined_students_names}) 

def class_base(request):
    return render(request,'class/base.html')

def open_workspace(request, workspace_id):
    single_workspace = WorkSpace.objects.filter(id=workspace_id)
    single_workis = WorkSpace.objects.get(id=workspace_id)
    memberships = Membership.objects.filter(workspace=single_workis).count()
    assignments = Assignment.objects.filter(workspace=single_workis).order_by('-created_at')
    return render(request,'class/single.html',{'joinees':memberships,'single_workspace':single_workspace,'single_works':single_workis,'assgnmt':assignments})

def view_sub(request, assignment_id):
    assignment = Assignment.objects.filter(id=assignment_id)
    assignments = Assignment.objects.get(id=assignment_id)
    workspace = assignments.workspace
    all_s= Membership.objects.filter(workspace=workspace)
    print(all_s)
    assigned = Membership.objects.filter(workspace=workspace).count()
    submission = Submission.objects.filter(assignment=assignments)
    submitted = submission.count()
    assignment_date = assignments.due_date
    all_students = Student.objects.filter(membership__workspace=workspace)
    print(all_students)
    not_submitted_students = []
    for student in all_students:
        if not submission.filter(student=student).exists():
            not_submitted_students.append(student)
    return render(request, 'class/view_submissions.html', {
        'not_submitted_students': not_submitted_students,
        'assignment_date': assignment_date,
        'assignment': assignment,
        'joinees': assigned,
        'submitted': submitted,
        'submissions': submission
        })

def index(request):
    return render(request,'index.html')

def base(request):
    return render(request,'base/base.html')

def send_mail(request):
    return render(request,'dashboard/teacher/send_mail.html')

def recieve_mail(request):
    return render(request,'dashboard/student/email.html')

  
