#models.py
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Lesson(models.Model):
    title = models.CharField(max_length=200, null=True)
    content_text = models.TextField(null=True, blank=True)
    content_image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class LessonDetail(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='lesson_details')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)  # To specify the order of lessons
    additional_content = models.TextField()

    def __str__(self):
        return f"{self.subject.name} - {self.lesson.title}"
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')])
    def __str__(self):
        return str(self.user)

class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, related_name='sub_categories',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name
class ClassName(models.Model):
    sub_class = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_classes', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name
# class CreateUserForm(UserCreationForm):
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
class AdminUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=False)
    name = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
# class AdminUserForm(forms.ModelForm):
#     class Meta:
#         model = AdminUser
#         fields = ['name', 'image']  # Add additional fields specific to the teacher model
class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=False)
    name = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
# class TeacherForm(forms.ModelForm):
#     class Meta:
#         model = Teacher
#         fields = ['name', 'image']  # Add additional fields specific to the teacher model
class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=False)
    name = models.CharField(max_length=200,null=True)
    classRoom = models.ManyToManyField(ClassName, related_name='student')
    rate = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True, blank=True)
    danh_hieu = models.ImageField(upload_to='student_danh_hieu/', null=True, blank=True)
    slot = models.IntegerField(default=0,null=True,blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    attendance = models.BooleanField(default=False)
    uploaded_file = models.FileField(upload_to='student_uploads/', null=True, blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['name', 'classRoom', 'rate', 'image', 'slot', 'teacher']

class Subject(models.Model):
    category = models.ManyToManyField(Category, related_name='subject')
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    develop = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    lessons = models.ManyToManyField('Lesson', through='LessonDetail')
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
class RegisSubject(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_Regis = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    # def __str__(self):
    #     return str(self.id)
    def __str__(self):
        return self.transaction_id
    @property
    def get_subject_item(self):
        subjectItems = self.regisSubjectItem_set.all()
        total = sum([item.quantity for item in subjectItems])
        return total
    @property
    def get_subject_total(self):
        subjectItems = self.regisSubjectItem_set.all()
        total = sum([item.get_total for item in subjectItems])
        return total
class RegisSubjectItem(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.SET_NULL,blank=True,null=True)
    regisSubject = models.ForeignKey(RegisSubject,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_regis = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        result = self.subject , self.regisSubject
        return str(result)

class StudentDetail(models.Model):
    customer = models.ForeignKey(Student,on_delete=models.SET_NULL,blank=True,null=True)
    regisSubject = models.ForeignKey(RegisSubject,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    mobile = models.CharField(max_length=10,null=True)
    date_regis = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address