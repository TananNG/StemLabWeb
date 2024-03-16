# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AdminUser, Teacher, Student

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['name', 'image']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'image']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'classRoom', 'rate', 'image','danh_hieu', 'slot', 'teacher', 'uploaded_file']


# Add other form classes as needed