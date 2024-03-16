# admin_views.py
from django.shortcuts import render, redirect
from .admin_forms import AddUserForm, AddTeacherForm, AddStudentForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda user: user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'admin', login_url='access_denied')
def admin_home(request):
    user = request.user
    student_form = AddStudentForm()
    teacher_form = AddTeacherForm()

    if request.method == 'POST':
        # Handle form submissions
        if user.profile.role == 'student':
            student_form = AddStudentForm(request.POST)
            if student_form.is_valid():
                # Process the form data for student
                # ...
                return redirect('admin_home')
        elif user.profile.role == 'teacher':
            teacher_form = AddTeacherForm(request.POST)
            if teacher_form.is_valid():
                # Process the form data for teacher
                # ...
                return redirect('admin_home')

    context = {
        'user': user,
        'student_form': student_form,
        'teacher_form': teacher_form,
    }
    return render(request, 'app/admin_home.html', context)
def add_user(request):
    if request.user.is_authenticated and request.user.profile.role == 'admin':
        if request.method == 'POST':
            form = AddUserForm(request.POST)
            role = request.POST.get('role')

            if form.is_valid():
                user = form.save()

                if role == 'student':
                    student_form = AddStudentForm(request.POST)
                    if student_form.is_valid():
                        student = student_form.save(commit=False)
                        student.user = user
                        student.save()
                        messages.success(request, f'Student {user.username} has been added successfully.')
                    else:
                        messages.error(request, f'Error adding student: {student_form.errors}')

                elif role == 'teacher':
                    teacher_form = AddTeacherForm(request.POST)
                    if teacher_form.is_valid():
                        teacher = teacher_form.save(commit=False)
                        teacher.user = user
                        teacher.save()
                        messages.success(request, f'Teacher {user.username} has been added successfully.')
                    else:
                        messages.error(request, f'Error adding teacher: {teacher_form.errors}')

                return redirect('admin_home')

        else:
            form = AddUserForm()

        return render(request, 'app/add_user.html', {'form': form})

    else:
        # Redirect or handle unauthorized access
        return redirect('access_denied')
def add_student(request):
    if request.method == 'POST':
        student_form = AddStudentForm(request.POST)
        if student_form.is_valid():
            # Process the form data for student
            user = student_form.save()  # This assumes your form is based on the User model
            # Additional logic for creating a student instance or other actions

            return redirect('admin_home')

    # If the form is not valid or it's a GET request, render the admin_home template
    return render(request, 'app/admin_home.html')

def add_teacher(request):
    if request.method == 'POST':
        teacher_form = AddTeacherForm(request.POST)
        if teacher_form.is_valid():
            # Process the form data for teacher
            user = teacher_form.save()  # This assumes your form is based on the User model
            # Additional logic for creating a teacher instance or other actions

            return redirect('admin_home')

    # If the form is not valid or it's a GET request, render the admin_home template
    return render(request, 'app/admin_home.html')