# admin_forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AdminUser, Teacher, Student

class AddUserForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('student', 'Student'), ('teacher', 'Teacher')])
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']

class AddTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'image']

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'classRoom', 'rate', 'image', 'slot', 'teacher']
