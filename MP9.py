admin.py
from django.contrib import admin
from studCourseRegApp.models import student, course

admin.site.site_header = 'FDP ON Django'
admin.site.site_title = 'FDP ON Django'

@admin.register(student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('usn', 'name')
    ordering = ('usn',)
    search_fields = ('name',)

@admin.register(course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseCode', 'courseName')
    ordering = ('courseCode',)
    search_fields = ('courseName',)


models.py

from django.db import models
from django.forms import ModelForm

class Course(models.Model):
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=50)
    course_credits = models.IntegerField()

    def __str__(self):
        return f"{self.course_code} {self.course_name} {self.course_credits}"

class Student(models.Model):
    usn = models.CharField(max_length=10)
    name = models.CharField(max_length=40)
    sem = models.IntegerField()
    courses = models.ManyToManyField(Course, related_name='student_set')

    def __str__(self):
        return f"{self.usn} {self.name} {self.sem}"

class ProjectRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=30)
    project_language = models.CharField(max_length=30)
    project_duration = models.IntegerField()

class ProjectForm(ModelForm):
    required_css_class = "required"

    class Meta:
        model = ProjectRegistration
        fields = ['student', 'project_title', 'project_language', 'project_duration']


python manage.py makemigrations
python manage.py migrate



import django.db.models.deletion
from django.db import migrations, models

from django.db import models
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('studCourseRegApp', '0001_initial'),
    ]
    
    operations = [
        migrations.CreateModel(
            name='ProjectReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptitle', models.CharField(max_length=30)),
                ('planguage', models.CharField(max_length=30)),
                ('pduration', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=models.CASCADE, to='studCourseRegApp.Student')),
            ],
        ),
    ]



python manage.py makemigrations
python manage.py migrate

views.py

from django.http import HttpResponse
from django.shortcuts import render
from studCourseRegApp.models import student, course, projectForm

def home(request):
    return render(request, 'home.html')

def student_list(request):
    students = student.objects.all()
    return render(request, 'studentlist.html', {'student_list': students})

def course_list(request):
    courses = course.objects.all()
    return render(request, 'courselist.html', {'course_list': courses})

def register(request):
    if request.method == "POST":
        student_id = request.POST.get("student")
        course_id = request.POST.get("course")
        student_obj = student.objects.get(id=student_id)
        course_obj = course.objects.get(id=course_id)
        result = student_obj.courses.filter(id=course_id)
        
        if result:
            response = "<h1>Student with USN %s has already enrolled for the %s</h1>" % (student_obj.usn, course_obj.courseCode)
            return HttpResponse(response)
        
        student_obj.courses.add(course_obj)
        response = "<h1>Student with USN %s successfully enrolled for the course with sub code %s</h1>" % (student_obj.usn, course_obj.courseCode)
        return HttpResponse(response)
    
    else:
        student_list = student.objects.all()
        course_list = course.objects.all()
        return render(request, 'register.html', {'student_list': student_list, 'course_list': course_list})

def enrolled_students(request):
    if request.method == "POST":
        course_id = request.POST.get("course")
        course_obj = course.objects.get(id=course_id)
        student_list_obj = course_obj.student_set.all()
        return render(request, 'enrolledlist.html', {'course': course_obj, 'student_list': student_list_obj})
    
    else:
        course_list = course.objects.all()
        return render(request, 'enrolledlist.html', {'Course_List': course_list})

def add_project(request):
    if request.method == "POST":
        form = projectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("<h1>Project Data Successfully saved</h1>")
    
    else:
        # Handle the else case appropriately
        pass


urls.py

from django.contrib import admin
from django.urls import path
from studCourseRegApp.views import enrolledStudentsUsingAjax, generateCSV, home, registerAjax, studentlist, courselist, register, enrolledStudents, add_project

urlpatterns = [
    path('secretadmin/', admin.site.urls),
    path('', home),
    path('home/', home),
    path('studentlist/', studentlist),
    path('courselist/', courselist),
    path('register/', register),
    path('enrolledlist/', enrolledStudents),
    path('addproject/', add_project),
]
