from django.db import models
from django.contrib.auth.models import UserManager
import datetime 
from django.utils.timezone import now
# Create your models here.
class Instructor(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length = 30)
    email = models.EmailField(max_length=254,unique=True)
    contact = models.CharField(max_length=10)
    password = models.CharField(max_length=100,default='abc123')
    address = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    
    def __str__(self):
    	return self.name

#course cid , cname, cdiscrpiton 

class Course(models.Model):
    coursename = models.CharField(max_length=50)
    #discription = models.TextField()
    instructor = models.ManyToManyField(Instructor)
    def __str__(self):
    	return self.coursename

class Topic(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.TextField()
    discription = models.TextField()
    def __str__(self):
    	return self.name

#Language lid , name  

class Language(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
    	return self.name

#batch bid ,bname
class Batch(models.Model):
    batchname = models.CharField(max_length=50,unique=True)
    instructor = models.ManyToManyField(Instructor)
    course = models.ManyToManyField(Course)
    def __str__(self):
    	return self.batchname

class Student(models.Model):
    studentname = models.CharField(max_length=30)
    city = models.CharField(max_length = 30)
    email = models.EmailField(max_length=254,unique=True)
    contact = models.CharField(max_length=10)
    semester = models.IntegerField()
    branch = models.CharField(max_length=30,default='Information Technology')
    password = models.CharField(max_length=100,default='abc123')
    batch = models.ForeignKey(Batch,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,default='Provide Address')
    course = models.ManyToManyField(Course)
    objects = UserManager()
    def __str__(self):
    	return self.studentname

class Assignment(models.Model):
    name = models.CharField(max_length=30)
    defination = models.CharField(max_length = 254)
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    student = models.ManyToManyField(Student)
    language = models.ManyToManyField(Language)
    batch = models.ManyToManyField(Batch)
    date = models.DateTimeField(default=now)
    def __str__(self):
    	return self.name

class Solution(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    status = models.CharField(max_length = 254,default="Not Submit") #submit or not status
    submission = models.BooleanField(default=False) #check only one submission allowed
    code = models.TextField(default='abc123')
    batch = models.ForeignKey(Batch,on_delete=models.SET_NULL,null=True)
    percentage = models.FloatField(default="0")
    autograde = models.CharField(max_length = 254,default="A")
    date = models.DateTimeField(default=now)
    def __str__(self):
    	return self.student.studentname

class SampleTestCase(models.Model):
    discription = models.TextField()
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    def __str__(self):
    	return self.assignment.name
        
class Testcase(models.Model):
    name = models.CharField(max_length = 254)
    input = models.CharField(max_length = 254)
    output = models.TextField()
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    testcasetype = models.CharField(max_length = 254)
    def __str__(self):
    	return self.name

class TestcaseOutput(models.Model):
    studentexpectedoutput =models.TextField(default="Not")
    studentcodeoutput = models.TextField(default="Not")
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    status = models.CharField(max_length = 254)
    testcase = models.ForeignKey(Testcase,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution,on_delete=models.CASCADE)
    def __str__(self):
    	return self.student.studentname

class Grade(models.Model):
    name = models.TextField(default="A")
    percentage = models.FloatField(default="0")
    solution = models.ForeignKey(Solution,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    def __str__(self):
    	return self.student.studentname

class TemporarySaveAssignmentData(models.Model):
    tempcode = models.TextField(default='abc123')
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    language = models.CharField(max_length = 254)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    counttab =models.IntegerField(default="0")


