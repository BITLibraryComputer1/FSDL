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


After writing models.py run the below commands in VS code terminal.
python manage.py makemigrations
python manage.py migrate


views.py

from django.http import HttpResponse
from django.shortcuts import render
from studCourseRegApp.models import student, course, projectForm
from django.views import generic
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table

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
        student_obj.courses.add(course_obj)
        response = "<h1>Student with USN %s successfully enrolled for the course with sub code %s</h1>" % (student_obj.usn, course_obj.courseCode)
        return HttpResponse(response)
    else:
        students = student.objects.all()
        courses = course.objects.all()
        return render(request, 'register.html', {'student_list': students, 'course_list': courses})

def enrolled_students(request):
    if request.method == "POST":
        course_id = request.POST.get("course")
        course_obj = course.objects.get(id=course_id)
        student_list_obj = course_obj.student_set.all()
        return render(request, 'enrolledlist.html', {'course': course_obj, 'student_list': student_list_obj})
    else:
        courses = course.objects.all()
        return render(request, 'enrolledlist.html', {'Course_List': courses})

def add_project(request):
    if request.method == "POST":
        form = projectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("<h1>Project Data Successfully saved</h1>")
    else:
        form = projectForm()
    return render(request, "projectReg.html", {'form': form})

class StudentListView(generic.ListView):
    model = student
    template_name = "GenericListViewStudent.html"

class StudentDetailView(generic.DetailView):
    model = student
    template_name = "GenericDetailedViewStudent.html"

def generate_csv(request):
    courses = course.objects.all()
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=course_data.csv'
    writer = csv.writer(response)
    writer.writerow(['Course Code', 'Course Name', 'Course Credits'])
    for c in courses:
        writer.writerow([c.courseCode, c.courseName, c.courseCredits])
    return response

def generate_pdf(request):
    courses = course.objects.all()
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=course_data.pdf'
    pdf = SimpleDocTemplate(response, pagesize=letter)
    table_data = [['Course Code', 'Course Name', 'Course Credits']]
    for c in courses:
        table_data.append([c.courseCode, c.courseName, str(c.courseCredits)])
    table = Table(table_data)
    pdf.build([table])
    return response


urls.py

from django.contrib import admin
from django.urls import path
from studCourseRegApp.views import enrolledStudentsUsingAjax, generateCSV, home, registerAjax, studentlist,courselist,register,enrolledStudents,add_project,StudentListView,StudentDetailView,generatePDF
urlpatterns = [
path('secretadmin/', admin.site.urls),
path('',home),
path('home/',home),
path('studentlist/',studentlist),
path('courselist/',courselist),
path('register/',register),
path('enrolledlist/',enrolledStudents),
path('addproject/',add_project),
path('genericlistviewstudent/',StudentListView.as_view()),
path('genericdetailedviewstudent/<int:pk>/',StudentDetailView.as_view()),
path('download_course_table_as_csv/',generateCSV),
path('download_course_table_as_pdf/',generatePDF),
]
