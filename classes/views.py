from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Classroom, Student
from .forms import ClassroomForm, StudentForm, SignupForm, SigninForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q

def acce(request):
    return render(request,"no-access.html")

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")




def classroom_list(request):
    classrooms = Classroom.objects.all()

    query = request.GET.get('q')
    if query:
        classrooms = classrooms.filter(
            Q(teacher__username__icontains=query)|
            Q(name__icontains=query)|
            Q(subject__icontains=query)|
            Q(year__icontains=query)

            ).distinct()


    context = {
        "classrooms": classrooms,
        "q": query
    }
    return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    students = Student.objects.filter(classroom=classroom).order_by('name', '-exam_grade')
    context = {
        "classroom": classroom,
        "students":students,
    }
    return render(request, 'classroom_detail.html', context)



def classroom_create(request):
    if not request.user.is_authenticated:
        return redirect('signin')   
    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user
            classroom.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    }
    return render(request, 'create_classroom.html', context)


def create_student(request, classroom_id):
    if not request.user.is_authenticated:
        return redirect('signin')
   
    form = StudentForm()
    classroom = Classroom.objects.get(id=classroom_id)
    if not request.user.username == classroom.teacher.username:
        return redirect('no-access') 
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom
            student.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-detail', classroom_id=classroom.id)
        print (form.errors)
    context = {
        "form":form,
        "classroom": classroom,

    }
    return render(request, 'create_student.html', context)



def student_update(request, student_id):
    student = Student.objects.get(id=student_id)
    form=StudentForm(instance = student)
    
    if not request.user.is_authenticated:
        return redirect('signin')
    if not request.user==student.classroom.teacher:
        return redirect('noaccess')
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-detail', student.classroom.id )
        print (form.errors)
    context = {
    "form": form,
    "student":student,
    }
    return render(request, 'update_student.html', context)


def student_delete(request, student_id):
    student = Student.objects.get(id=student_id)
    returnid= student.classroom.id
    
    if not request.user.is_authenticated:
        return redirect('signin')
    if not request.user==student.classroom.teacher:
        return redirect('noaccess')
    student.delete()
    return redirect('classroom-detail', returnid )

def classroom_update(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')    
    classroom = Classroom.objects.get(id=classroom_id)
    if not(request.user.is_staff or request.user == classroom.teacher):
        return redirect('no-access') 
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)

def classroom_delete(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')
    if not request.user.is_staff:
        return redirect('no-access')    
    Classroom.objects.get(id=classroom_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')
