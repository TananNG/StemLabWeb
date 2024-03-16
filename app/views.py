#views.py
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.template import RequestContext
from app.admin_forms import AddStudentForm, AddTeacherForm, AddUserForm

from app.form import CreateUserForm, TeacherForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

# Create your views here.

def category(request):
    if request.user.is_authenticated:

        user_not_login = 'hidden'
        user_login = 'show'
    else:
        user_not_login = 'show'
        user_login = 'hidden'
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        subjects = Subject.objects.filter(category__slug= active_category)
    context={'categories':categories,'subjects':subjects,'active_category':active_category, 'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/category.html',context)
# def classname(request):
#     if request.user.is_authenticated:

#         user_not_login = 'hidden'
#         user_login = 'show'
#     else:
#         user_not_login = 'show'
#         user_login = 'hidden'
#     if request.user.profile.role != 'teacher':
#         return redirect('home')
#     classes = ClassName.objects.filter(is_sub = False)
#     active_classname = request.GET.get('classname', '')
#     students = None  # Khởi tạo biến students
#     if active_classname:
#         # Truy vấn danh sách học sinh thuộc lớp có tên là active_classname
#         students = Student.objects.filter(classRoom__slug=active_classname)
        
#     context = {'classes': classes, 'students': students, 'active_classname': active_classname, 'user_not_login': user_not_login, 'user_login': user_login}
#     return render(request, 'app/classname.html', context)
@login_required(login_url='login')
def classname(request):
    user_not_login = 'hidden'
    user_login = 'show'
    
    if request.user.profile.role != 'teacher':
        return redirect('home')
    categories = Category.objects.filter(is_sub = False)
    teacher = request.user.teacher  # Assuming each teacher has a one-to-one relationship with User
    
    if teacher:
        classes = ClassName.objects.filter(is_sub=False, sub_class=None)
        active_classname_slug = request.GET.get('classname', '')
        students = None

        if active_classname_slug:
            # Retrieve the ClassName object for the active class
            active_class = get_object_or_404(ClassName, slug=active_classname_slug)

            # Filter students based on the class and teacher association
            students = Student.objects.filter(classRoom=active_class, teacher=teacher)

        context = {
            'classes': classes,
            'students': students,
            'active_classname_slug': active_classname_slug,
            'user_not_login': user_not_login,
            'user_login': user_login,
            'categories':categories
        }

        return render(request, 'app/classname.html', context)
    else:
        # Handle the case when the logged-in user is not associated with any teacher
        return render(request, 'app/no_teacher_assigned.html')

def home(request):
    if request.user.is_authenticated:

        user_not_login = 'hidden'
        user_login = 'show'
    else:
        user_not_login = 'show'
        user_login = 'hidden'
    categories = Category.objects.filter(is_sub = False)
    classes = ClassName.objects.filter(is_sub = False)
    #active_category = request.GET.get('category','')
    subjects = Subject.objects.all()
    
    context= {'user': request.user,'subjects': subjects,'user_not_login':user_not_login,'user_login':user_login,'categories':categories,'classes':classes}
    return render(request,'app/home.html',context)
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Subject.objects.filter(name__contains=searched)
        context={'searched':searched,'keys':keys,}
    return render(request,'app/search.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'user or password is incorrect!')
    
    return render(request,'app/login.html')
def logoutPage(request):
    logout(request)
    return redirect('login')
# def register(request):
#     form = CreateUserForm()
#     if request.method == "POST":
#         form =CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#         else:
#             return redirect('register')
#     context = {'form':form}
#     return render(request,'app/register.html',context)

def register(request):
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        role = request.POST.get('role')
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user, role=role)

            if role == 'student':
                teacher_id = request.POST.get('teacher')
                teacher = Teacher.objects.get(id=teacher_id)
                Student.objects.create(user=user, teacher=teacher)
                # Additional logic for student registration

            elif role == 'teacher':
                teacher_form = TeacherForm(request.POST)
                if teacher_form.is_valid():
                    teacher = teacher_form.save(commit=False)
                    teacher.user = user
                    teacher.save()
                    # Additional logic for teacher registration

            login(request, user)
            return redirect('home')
    else:
        form = CreateUserForm()
        teacher_form = TeacherForm()

    return render(request, 'app/register.html', {'form': form, 'teacher_form': teacher_form, 'teachers': teachers}) 
# def classroom(request):
#     if request.user.is_authenticated:
#         user = request.user
#         students, created = Student.objects.get_or_create(user=user)
        
#         # Now you can access all students related to the user
#         students = Student.objects.filter(user=user)
        
#     else:
#         students = []
    
#     context = {'students': students}
#     return render(request, 'app/classroom.html', context)


def classroom(request):
    user_not_login = 'hidden'
    user_login = 'show'
    students = []
    subject_data = []
    
    if request.user.is_authenticated:
        user = request.user
        student, created = Student.objects.get_or_create(user=user)
        students = Student.objects.filter(user=user)

        # Iterate through students to get registration subjects and associated subject data
        
            # Get the registration subjects for the student
        registration_subjects = RegisSubject.objects.filter(customer=user)
            
            # Iterate through registration subjects and get the associated subject data
        for regis_subject in registration_subjects:
            regis_subject_items = RegisSubjectItem.objects.filter(regisSubject=regis_subject)
            for regis_subject_item in regis_subject_items:
                subject_data.append({
                    'subject_name': regis_subject_item.subject.name,
                    'quantity': regis_subject_item.quantity,
                })

    else:
        user_not_login = 'show'
        user_login = 'hidden'

    categories = Category.objects.filter(is_sub=False)
    context = {
        'categories': categories,
        'students': students,
        'subject_data': subject_data,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'app/classroom.html', context)
@user_passes_test(lambda user: user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'teacher', login_url='access_denied')
def mark_attendance(request):
    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_students')

        for student_id in selected_students:
            student = get_object_or_404(Student, id=student_id)

            # Increment the slot value by 1
            student.slot += 1

            # If the slot exceeds 24, reset it to 1
            if student.slot > 24:
                student.slot = 1

            # Save the student object
            student.save()

            # You can add additional logic here if needed

        # Render the mark_attendance.html template (if you have one)
        return render(request, 'app/mark_attendance.html')

    return HttpResponse("Invalid request")
@user_passes_test(lambda user: user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'teacher', login_url='access_denied')
def rate_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        new_rating = request.POST.get('rating')
        student.rate = new_rating
        student.save()

    context = {'student': student}
    return render(request, 'app/rate_student.html', context)
def students(request):
    context= {}
    return render(request,'app/student.html',context)
@login_required(login_url='login')
def learn_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    categories = Category.objects.filter(is_sub = False)
    context = {'subject': subject,'categories':categories}
    return render(request, 'app/learn_subject.html', context)
def lesson_detail(request, subject_id, lesson_index):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if subject.lessons:
        lessons = subject.lessons.all()

        if 0 <= lesson_index < len(lessons):
            lesson = lessons[lesson_index]
            lesson_number = lesson_index + 1  # Perform the addition here
            context = {'subject': subject, 'lesson': lesson, 'lesson_number': lesson_number}
            return render(request, 'app/lesson_detail.html', context)
    

    return render(request, 'app/lesson_not_found.html')

def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    context = {'subject': subject}
    return render(request, 'app/subject_detail.html', context)
def your_view(request):
    # Các xử lý khác của view
    return render(request, 'your_template.html', context_instance=RequestContext(request))
def access_denied(request):
    return render(request, 'app/access_denied.html')
