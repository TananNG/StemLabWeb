#urls.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from . import views
from .admin_views import add_user
from app import admin_views
urlpatterns = [
    path('', views.home, name="home"),
    path('class/', views.classroom, name="class"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.register, name="register"),
    path('student/', views.students, name="student"),
    path('search/', views.search, name="search"),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('subject/<int:subject_id>/learn/', views.learn_subject, name='learn_subject'),
    path('subject/<int:subject_id>/lesson/<int:lesson_index>/', views.lesson_detail, name='lesson_detail'),
    path('category/', views.category, name="category"),
    
    path('classname/', views.classname, name="classname"),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('rate_student/<int:student_id>/', views.rate_student, name='rate_student'),
    path('access_denied/', views.access_denied, name='access_denied'),
    path('add_user/', admin_views.add_user, name='add_user'),
    path('admin_home/', admin_views.admin_home, name='admin_home'),
    path('add_student/', admin_views.add_student, name='add_student'),
    path('add_teacher/', admin_views.add_teacher, name='add_teacher'),
    
]