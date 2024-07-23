models.py

from django.db import models
from django.forms import ModelForm
# Create your models here.
class course(models.Model):
    courseCode=models.CharField(max_length=10)
    courseName=models.CharField(max_length=50)
    courseCredits=models.IntegerField()
    def __str__(self):
        return self.courseCode+" "+self.courseName+" "+str(self.courseCredits)

class student(models.Model):
    usn=models.CharField(max_length=10)
    name=models.CharField(max_length=40)
    sem=models.IntegerField()
    courses=models.ManyToManyField(course,related_name='student_set')

    def __str__(self):
        return self.usn+" "+self.name+" "+str(self.sem)

python manage.py makemigrations
python manage.py migrate

s1=student(usn= ‘1BI21CS001’,name= ‘Harish’, sem=6)
s2=student(usn= ‘1BI21CS002’,name= ‘Kumar’, sem=6)
s3=student(usn= ‘1BI21CS003’,name= ‘Chetan, sem=6)
s4=student(usn= ‘1BI21CS004’,name= ‘Rama’, sem=6)
s5=student(usn= ‘1BI21CS005’,name= ‘Krishna, sem=6)
s6=student(usn= ‘1BI21CS007’,name= ‘XYZ, sem=6)
studList=[s1,s2,s3,s4,s5,s6]
for stud in studList:
	stud.save()
c1=course(courseCode='21CS61',courseName='SE',courseCredits=3)
c2=course(courseCode='21CS62',courseName='FSD',courseCredits=3)
c3=course(courseCode='21CS63',courseName='CGV',courseCredits=3)
c4=course(courseCode='21CS64',courseName='DBMS',courseCredits=3)
c5=course(courseCode='21CSL62',courseName='FSD Lab',courseCredits=2)
courseList=[c1,c2,c3,c4,c5]
for course in courseList:
	course.save()
	

views.py

from django.http import HttpResponse
from django.shortcuts import render
from studCourseRegApp.models import student,course, projectForm
# Create your views here.
def home(request):
    return render(request,'home.html')
def studentlist(request):
    s=student.objects.all()
    return render(request,'studentlist.html',{'student_list':s})
def courselist(request):
    c=course.objects.all()
    return render(request,'courselist.html',{'course_list':c})
def register(request):
    if request.method=="POST":
        sid=request.POST.get("student")
        cid=request.POST.get("course")
        studentobj=student.objects.get(id=sid)
        courseobj=course.objects.get(id=cid)
        res=studentobj.courses.filter(id=cid)
        if res:
            resp="<h1>Student with usn %s has already enrolled for the %s<h1>"%(studentobj.usn,courseobj.courseCode)
            return HttpResponse(resp)
        studentobj.courses.add(courseobj)
        resp="<h1>student with usn %s successfully enrolled for the course with sub code %s</h1>"%(studentobj.usn,courseobj.courseCode)
        return HttpResponse(resp)
    else:
        studentlist=student.objects.all()
        courselist=course.objects.all()
        return render(request,'register.html',{'student_list':studentlist,'course_list':courselist})

def enrolledStudents(request):
    if request.method=="POST":
        cid=request.POST.get("course")
        courseobj=course.objects.get(id=cid)
        studentlistobj=courseobj.student_set.all()
        return render(request,'enrolledlist.html',{'course':courseobj,'student_list':studentlistobj})
    else:
        courselist=course.objects.all()
        return render(request,'enrolledlist.html',{'Course_List':courselist})

urls.py
from django.contrib import admin
from django.urls import path
from studCourseRegApp.views import home, studentlist,courselist,register,enrolledStudents
urlpatterns = [
    path('secretadmin/', admin.site.urls),
    path('',home),
    path('home/',home),
    path('studentlist/',studentlist),
    path('courselist/',courselist),
    path('register/',register),
    path('enrolledlist/',enrolledStudents),
]