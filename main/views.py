import csv,io
import ast
from django.utils.timezone import now
from django.core.mail import send_mail
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import *
from .models import *
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.template import Context, loader
from urllib.error import HTTPError
import json
import http.client
import datetime
from time import gmtime, strftime
RUNS_RESOURCE = '/jobe/index.php/restapi/runs/'
JOBE_SERVER = 'localhost'
USE_API_KEY = True
API_KEY = '2AAA7A5415B4A9B394B54BF1D2E9D'
DEBUGGING = False
GOOD_TEST = "Test Case is Pass"
FAIL_TEST = "Test Case is Fail"
EXCEPTION = "Test Case generate Exception"
VERBOSE = False
studentouput = ""
percentage = 0
studentexpectedtouput = ""
# Create your views here.
def email(request):
    if request.method == "POST":
        email =request.POST['email']
        name = request.POST['name']
        email_title = email + ' from ' + name
        message = request.POST['message']
        subject  = request.POST['subject']
        email_body = """
        Name: """+name+"""
        subject:"""+subject+"""
        message:"""+message+"""
        email: """+email
        print(email_title)
        print(email_body)
        send_mail(email_title, email_body, 'autogradingsystem99999@gmail.com',['autogradingsystem99999@gmail.com'],fail_silently=False)
        email_reply_title="""Thank you for contacting to Auto Grading System"""
        email_reply_body = """
        Auto Grading System team solve your query as soon as possible
        
        Thank you 
        """+name
        send_mail(email_reply_title, email_reply_body, email,[email],fail_silently=False)
        return render(request,'homepage/email.html')
    else:
        return render(request,'homepage/email.html')



def ForgotPassword(request):
    if 'studentmailid' in request.session:
        del request.session['studentmailid']
    return render(request,"homepage/password_reset.html")

def PasswordResetDone(request):
    if request.method == "POST":
        try:
            email =request.POST['email']
            print(email)
            student = Student.objects.get(email= email)
            email_body = """
            Thanks for using our site!

            Please use this link is only for forget password

            You're receiving this email because you requested a password reset for your user account at AutoGradingSystem.

            Your username is email in case you’ve forgotten

            Please go to the following page and choose a new password:

            http://localhost:8000/autogradingforgotpassword/"""+str(student.id) 
            email_title = "Hello " + str(student.studentname)
            request.session['studentmailid'] = student.id
            print(request.session['studentmailid'])
            send_mail(email_title, email_body, email,[email],fail_silently=False)
            return render(request,"homepage/password_reset_done.html")
        except:
            email =request.POST['email']
            print(email)
            print("Email is not found")
            messages.info(request,"Email does not exits")
            return redirect("/ForgotPassword")
    else:
        if'studentmailid' in request.session:
            return render(request,"homepage/password_reset_done.html")
        else:
            messages.info(request,"Please Enter your email first for forgot password")
            return render(request,"homepage/password_reset.html")  

def autogradingforgotpassword(request,sid):
    try:
        if 'studentmailid' in request.session:
            print(request.session['studentmailid'])       
            studentmailid = int(request.session['studentmailid'])
            if int(sid)  == studentmailid:
                context = {
                    'sid':sid,
                }
                return render(request,"homepage/password_reset_confirm.html",context)
            else:
                messages.info(request,"Please Enter your email first for forgot password")
                return render(request,"homepage/password_reset.html")
        else:
            messages.info(request,"Please Enter your email first for forgot password")
            return render(request,"homepage/password_reset.html")
    except:
        messages.info(request,"Please Enter your email first for forgot password")
        return render(request,"homepage/password_reset.html")  

def PasswordUpdate(request):
    if request.method == "POST":
        sid = request.POST['sid']
        password = request.POST['password']
        student = Student.objects.get(id=sid)
        student.password = password
        student.save()
        return render(request,"homepage/password_reset_complete.html")
    else:
        return render(request,"homepage/password_reset_complete.html")

def error404(request,exception):
    return render(request,"error/404.html")

def homepage(request):
    print(datetime.datetime.now())
    print(datetime.datetime.now().time())
    print(datetime.date.today())
    return render(request,"homepage/index.html")

def loginpage(request):
    return render(request,"homepage/login.html")

def authenticate(request):
    if 'email' in request.session:
        try:
            email = request.session['email']
            student = Student.objects.get(email=email)
            return redirect("/StudentProfile")
        except:
            messages.info(request,'Password or Username Wrong')
            return redirect("/login")
            

    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        students = Student.objects.all()

        if students is not None:
            for student in students:
                if student.password == password and student.email == username:
                    print("succsess")
                    request.session['email'] = student.email
                    return redirect("/StudentCourse")

    messages.info(request,'Password or Username Wrong')
    return redirect("/login")

def StudentProfile(request):
    if 'email' in request.session:
        email = request.session['email']
        student = Student.objects.get(email=email)
        return render(request,"Student/StudentDashboard.html",{'student':student})
        

    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        students = Student.objects.all()

        if students is not None:
            for student in students:
                if student.password == password and student.email == username:
                    print("succsess")
                    request.session['email'] = student.email
                    return render(request,"Student/StudentDashboard.html",{'student':student})

    messages.info(request,'Password or Username Wrong')
    return redirect("/login")


def Logout(request):
    try:
        del request.session['email']
        return redirect("/")
    except:
         return redirect("/")

def StudentEdit(request):
    if 'email' in request.session:
        try:
            email = request.session['email']
            student = Student.objects.get(email=email)
            return render(request,"Student/StudentProfileEdit.html",{'student':student})
        except:
            messages.info(request,'Password or Username Wrong')
            return redirect("/login")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")

def StudentChange(request):
    if 'email' in request.session:
        try:
            email = request.session['email']
            student = Student.objects.get(email=email)
            student.studentname = request.POST["name"]
            student.city = request.POST["city"]
            student.contact = request.POST["contact"]
            student.semester = request.POST["semester"]
            student.branch = request.POST["branch"]
            student.password =request.POST["password"]
            student.address = request.POST["address"]
            student.save()
            messages.info(request,'Profile Update Successfully')
            return render(request,"Student/StudentDashboard.html",{'student':student})
        except:
            return redirect("/Dashboard")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")

def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def InstructorLogin(request):
    return render(request,"Instructor/InstructorLogin.html")

def InstructorDashboard(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        return render(request,"Instructor/InstructorDashboard.html",{'instructor':instructor})

    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        instructors = Instructor.objects.all()

        if instructors is not None:
            for instructor in instructors:
                if instructor.password == password and instructor.email == username:
                    print("succsess")
                    request.session['username'] = instructor.email
                    return redirect("/InstructorCourse")

    messages.info(request,'Password or Username Wrong')
    return redirect("/InstructorLogin")
    
def InstructorProfile(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        return render(request,"Instructor/InstructorDashboard.html",{'instructor':instructor})

    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        instructors = Instructor.objects.all()

        if instructors is not None:
            for instructor in instructors:
                if instructor.password == password and instructor.email == username:
                    print("succsess")
                    request.session['username'] = instructor.email
                    return render(request,"Instructor/InstructorDashboard.html",{'instructor':instructor})

    messages.info(request,'Password or Username Wrong')
    return redirect("/InstructorLogin")

def InstructorEdit(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        return render(request,"Instructor/InstructorProfileEdit.html",{'instructor':instructor})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorChange(request):
    if 'username' in request.session:
        try:
            email = request.session['username']
            instructor = Instructor.objects.get(email=email)
            instructor.name = request.POST["name"]
            instructor.city = request.POST["city"]
            instructor.contact = request.POST["contact"]
            instructor.position = request.POST["position"]
            instructor.qualification = request.POST["qualification"]
            instructor.password =request.POST["password"]
            instructor.address = request.POST["address"]
            instructor.save()
            messages.info(request,'Profile Update Successfully')
            return render(request,"Instructor/InstructorDashboard.html",{'instructor':instructor})
        except:
            return redirect("/InstructorDashboard")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")
    
def InstructorLogout(request):
    try:
        del request.session['username']
        return redirect("/")
    except:
        return redirect("/")

def InstructorCourse(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        courses = Course.objects.all()
        return render(request,"Instructor/InstructorCourse.html",{'courses':courses,'curinstructor':instructor})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def StudentCourse(request):
    if 'email' in request.session:
        try:
            email = request.session['email']
            student = Student.objects.get(email=email)
            return render(request,"Student/StudentCourse.html",{'student':student})
        except:
            messages.info(request,'Password or Username Wrong')
            return redirect("/login")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")

def InstructorCourseDelete(request,id):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        obj = get_object_or_404(Course,id=id)
        obj.delete()
        courses = Course.objects.all()
        messages.info(request,'Course Deleted SuccessFully')
        return redirect('/InstructorCourse')
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorCourseEdit(request,id):
    if 'username' in request.session:
        email = request.session['username']
        request.session['courseid'] = id
        instructor = Instructor.objects.get(email=email)
        course = Course.objects.get(id=id)
        return redirect("/InstructorCourseEditPageShow")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorCourseEditPageShow(request):
    if 'username' in request.session:
        email = request.session['username']
        if 'courseid' in request.session:
            id = request.session['courseid'] 
            instructor = Instructor.objects.get(email=email)
            course = Course.objects.get(id=id)
            return render(request,'Instructor/InstructorCourseEdit.html',{'course':course,'curinstructor':instructor})
        else:
            return redirect("/InstructorDashboard")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InsructorCourseChange(request):
    if 'username' in request.session:
        email = request.session['username']
        if 'courseid' in request.session:
            id = request.session['courseid'] 
            instructor = Instructor.objects.get(email=email)
            course = Course.objects.get(id=id)
            course.coursename = request.POST['coursename']
            #course.discription = request.POST['discription']
            course.save()
            messages.info(request,'Course Update Successfully')
            allcourses = Course.objects.all()
            return render(request,"Instructor/InstructorCourse.html",{'courses':allcourses,'curinstructor':instructor})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorCourseCreate(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        return render(request,"Instructor/InstructorCourseCreate.html",{'curinstructor':instructor})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstuctorCourseNew(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        if request.method == 'POST':
            cname = request.POST['coursename']
            instructor = Instructor.objects.get(email=email)
            instance = Course.objects.create(coursename=cname)
            instance.instructor.add(instructor)
           
            courses = Course.objects.all()
            messages.info(request,"New course Added Successfully")
            return render(request,"Instructor/InstructorCourse.html",{'courses':courses,'curinstructor':instructor})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def StudentCourseDetails(request,id):
    if 'email' in request.session:
        email = request.session['email']
        try:
            student = Student.objects.get(email=email)
            request.session['studentcourseid'] = id
            return redirect("/ShowStudentCourseDetails")
        except:
            messages.info(request,'Password or Username Wrong')
            return redirect("/login")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")



def ShowStudentCourseDetails(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            student = Student.objects.get(email=email)
            if 'studentcourseid' in request.session:
                id = request.session['studentcourseid'] 
                course = Course.objects.get(id=id)
                topic = Topic.objects.filter(course_id__pk=id)
                context = {
                    'course':course,
                    'topics':topic
                }
            return render(request,"Student/StudentCourseDetails.html",context)
        except:
            messages.info(request,'Password or Username Wrong')
            return redirect("/login")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")
    
def InstructorCourseDetails(request,id):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        request.session['instructorcourseid'] = id
        return redirect("/ShowInstructorCourseDetails")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def ShowInstructorCourseDetails(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        if 'instructorcourseid' in request.session:
            id = request.session['instructorcourseid'] 
            course = Course.objects.get(id=id) 
            topic = Topic.objects.filter(course_id__pk=id)  
            context = {
                    'course':course,
                    'topics':topic,
                    'curinstructor':instructor
                }
            return render(request,"Instructor/InstructorCourseDetails.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorStudentPage(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        studentslist = Student.objects.all()
        semesterlist = []
        for student in studentslist:
            if student.semester not in semesterlist:
                semesterlist.append(student.semester)
        batches = Batch.objects.all()
        return render(request,"Instructor/InstructorStudent.html",{'Students':studentslist,'curinstructor':instructor,'batches':batches,'semesterlist':semesterlist})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")


def InstructorStudentView(request,id):
     if 'username' in request.session:
        email = request.session['username']
        request.session['instructorsudentviewid'] = id
        instructor = Instructor.objects.get(email=email)
        #student = Student.objects.get(id=id)
        return redirect("/InstructorStudentViewpage")
     else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorStudentViewpage(request):
     if 'username' in request.session:
        email = request.session['username']
        if 'instructorsudentviewid' in request.session:
            id = request.session['instructorsudentviewid']
            instructor = Instructor.objects.get(email=email)
            student = Student.objects.get(id=id)
            return render(request,"Instructor/InstructorStudentView.html",{'student':student,'curinstructor':instructor})
     else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorCreateStudent(request):
     if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        batches = Batch.objects.all()
        return render(request,"Instructor/InstructorStudentCreate.html",{'curinstructor':instructor,'batches':batches})
     else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorUploadFile(request):
    if 'username' in request.session:
        prompt ={
            ''
        }
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        csv_file = request.FILES['fileupload']
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'Please Enter a valid CSV file')
            return render(request,'Instructor/InstructorCreateStudent.html')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        batchid = request.POST['batch']
        semester = request.POST['semester']
        print(semester)
        batchinstance = Batch.objects.get(id=batchid)
        courses = batchinstance.course.all()
        for column in csv.reader(io_string,delimiter=',',quotechar="|"):
            batch = Batch.objects.get(id=batchid)
            print(batch)
            try:
                students = Student.objects.get(email=column[2])
                students.studentname = column[0]
                students.city = column[1]
                students.email = column[2]
                students.contact = column[3]
                students.semester = semester
                students.branch = column[4]
                students.password = column[5]
                students.batch = batch
                students.address = column[6]
                students.save()
                msg = students.studentname+" data is Updated"
                messages.info(request,msg)
                continue
            except:
                try:
                    _,created = Student.objects.update_or_create(
                        studentname = column[0],
                        city = column[1],
                        email = column[2],
                        contact = column[3],
                        semester = semester,
                        branch = column[4],
                        password = column[5],
                        batch = batch,
                        address = column[6]
                    )
                    print("ok")
                    msg1 = column[0]+" data is Created"
                    messages.info(request,msg1)
                except:
                    messages.info(request,'file upload error')
                    return redirect("/InstructorCreateStudent")
        studentlist = Student.objects.filter(batch_id__pk=batchid)
        
        for student in studentlist:
            student.course.clear()
        for student in studentlist:
            for course in courses:
                student.course.add(course)
                student.save()
        batch = Batch.objects.get(id=batchid)
        assignments = Assignment.objects.filter(batch=batch)
        for assignment in assignments:
             for student in studentlist:
                 assignment.student.add(student)
            
            
        return redirect("/InstructorStudentPage")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorAssignCourse(request,id):
    if 'username' in request.session:
        email = request.session['username']
        # student = Student.objects.get(id=id)
        # instructor = Instructor.objects.get(email=email)
        # course = Course.objects.all()
        request.session['InstructorAssignCourseid'] = id
        #return render(request,"Instructor/InstructorAssignCourse.html",{'student':student,'curinstructor':instructor,'courses':course})
        return redirect("/InstructorAssignCoursepage")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorAssignCoursepage(request):
    if 'username' in request.session:
        email = request.session['username']
        if 'InstructorAssignCourseid' in request.session:
            id = request.session['InstructorAssignCourseid']
            student = Student.objects.get(id=id)
            instructor = Instructor.objects.get(email=email)
            course = Course.objects.all()
            return render(request,"Instructor/InstructorAssignCourse.html",{'student':student,'curinstructor':instructor,'courses':course})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")



def InstructorAssignCourseToStudent(request):
     if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        courseid = request.POST.getlist('course[]')
        if 'InstructorAssignCourseid' in request.session:
            sid = request.session['InstructorAssignCourseid']
            student = Student.objects.get(id=sid)
        for id in courseid:
            coursex = Course.objects.get(id=id)
            student.course.add(coursex)
        messages.info(request,"Course added Successfully to Student")
        return redirect("/InstructorStudentPage")
     else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")


def InstructorStudentDelete(request,id):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        student = Student.objects.get(id=id)
        student.delete()
        messages.info(request,"Student Deleted Successfully")
        return redirect("/InstructorStudentPage")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorStudentDeleteCourseShow(request,id):
    if 'username' in request.session:
        email = request.session['username']
        request.session["InstructorStudentDeleteCourseShowid"] = id
        instructor = Instructor.objects.get(email=email)
        return redirect("/InstructorStudentDeleteCourseShowpage")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorStudentDeleteCourseShowpage(request):
    if 'username' in request.session:
        email = request.session['username']
        if 'InstructorStudentDeleteCourseShowid' in request.session:
            id = request.session["InstructorStudentDeleteCourseShowid"]
            instructor = Instructor.objects.get(email=email)
            student = Student.objects.get(id=id)
            course = student.course.all()
            return render(request,"Instructor/InstructorStudentDeleteCourseShow.html",{'student':student,'curinstructor':instructor,'courses':course})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorAssignCourseToStudentdelete(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        courseid = request.POST.getlist('course[]')
        if 'InstructorStudentDeleteCourseShowid' in request.session:
            sid = request.session['InstructorStudentDeleteCourseShowid']
            student = Student.objects.get(id=sid)
        for id in courseid:
            coursex = Course.objects.get(id=id)
            student.course.remove(coursex)
        messages.info(request,"Course Unassign Successfully to Student")
        return redirect("/InstructorStudentPage")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorBatch(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        batchlist = Batch.objects.all()
        return render(request,"Instructor/InstructorBatch.html",{'batches':batchlist,'curinstructor':instructor})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorCreateBatch(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        courses = Course.objects.all()
        semesterlist = []
        students = Student.objects.all()
        for student in students:
            if student.semester not in semesterlist:
                semesterlist.append(student.semester)
        return render(request,"Instructor/InstructorBatchCreate.html",{'curinstructor':instructor,'courses':courses,'semesterlist':semesterlist})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorCreateBatchSubmit(request):
    if 'username' in request.session:
        email = request.session['username']
        batchname = request.POST['batchname']
        studentidlist = request.POST.getlist('student[]')
        print(studentidlist)
        print(batchname)
        try:
            batch = Batch.objects.get(batchname=batchname)
            messages.info(request,"Batch Name is already taken  ")
            return redirect("/InstructorCreateBatch")
        except:
            instructor = Instructor.objects.get(email=email)
            courselistid = request.POST.getlist('course[]')
            batchinstance = Batch.objects.create(batchname=batchname)
            batchinstance.instructor.add(instructor)
            for couseid in courselistid:
                course = Course.objects.get(id=couseid)
                batchinstance.course.add(course)
            for studentid in studentidlist:
                student = Student.objects.get(id=studentid)
                student.course.clear()
            for couseid in courselistid:
                course = Course.objects.get(id=couseid)
                for studentid in studentidlist:
                    student = Student.objects.get(id=studentid)
                    student.course.add(course)
                    student.save()
            for studentid in studentidlist:
                student = Student.objects.get(id=studentid)
                student.batch=batchinstance
                student.save()
            
            messages.info(request,"Batch Created Successfully")
            return redirect("/InstructorBatch")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")



def InstructorBatchEdit(request,id):
    if 'username' in request.session:
        email = request.session['username']
        request.session['batchid'] = id
        instructor = Instructor.objects.get(email=email)
        return redirect("/InstructorBatchEditPageShow")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorBatchEditPageShow(request):
    if 'username' in request.session:
        email = request.session['username']
        if 'batchid' in request.session:
            id = request.session['batchid'] 
            batch = Batch.objects.get(id=id)
            instructor = Instructor.objects.get(email=email)
            courses = Course.objects.all()
            instructors = Instructor.objects.all()
            studentlist = Student.objects.all()
            students = Student.objects.all()
            semesterlist = []
            for student in studentlist:
                if student.semester not in semesterlist:
                    semesterlist.append(student.semester)
            return render(request,"Instructor/InstructorBatchEdit.html",{'students':students,'semesterlist':semesterlist,'instructors':instructors,'curinstructor':instructor,'courses':courses,'batch':batch})
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorEditBatchSubmit(request):
    if 'username' in request.session:
        if 'batchid' in request.session:
            id = request.session['batchid']
            email = request.session['username']
            batchname = request.POST['batchname']
            studentidlist = request.POST.getlist('student[]')
            studentlist = Student.objects.filter(batch_id__pk=id)
            
            batch = Batch.objects.get(id=id)
            batch.batchname = batchname
            batch.instructor.clear()

            for student in studentlist:
                student.course.clear()

            curinstructor = Instructor.objects.get(email=email)
            batch.instructor.add(curinstructor)

            instructorlist =request.POST.getlist('instructor[]')
            for instructorid in instructorlist:
                instance = Instructor.objects.get(id=instructorid)
                batch.instructor.add(instance)

            courselistid = request.POST.getlist('course[]')

    
            instructor = Instructor.objects.get(email=email)
            removecourselist = Course.objects.filter(instructor=instructor)
            for course in removecourselist:
                batch.course.remove(course)
                
            for studentid in studentidlist:
                student = Student.objects.get(id=studentid)
                student.course.clear()
                student.save()

            for studentid in studentidlist:
                student = Student.objects.get(id=studentid)
                for courseid in courselistid:
                    course = Course.objects.get(id=courseid)
                    student.course.add(course)
                    student.save()

            for courseid in courselistid:
                course = Course.objects.get(id=courseid)
                batch.course.add(course)
            courselist =batch.course.all()
            for student in studentlist:
                for course in courselist:
                    student.course.add(course)
                    student.save()

            batch.save()

            for studentid in studentidlist:
                student = Student.objects.get(id=studentid)
                student.batch=batch
                student.save()
            messages.info(request,"Batch Updated Successfully")
            return redirect('/InstructorBatch')        
            #except:
                #url = '/InstructorBatchEdit/'+id
               # messages.info(request,"Batch Name is already taken")
                #return redirect(url)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstuructorStudentFilter(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        try: 
            sem = request.POST['semester']
            batchid = request.POST['batch']
            if batchid != 'NotAssign' and sem != 'ALL':
                studentsemetsterlist = Student.objects.all()
                studentslist = Student.objects.filter(semester=sem,batch=batchid)
                semesterlist = []
            elif batchid == 'NotAssign' and sem != 'ALL':
                studentsemetsterlist = Student.objects.all()
                studentslist = Student.objects.filter(semester=sem,batch=None)
                semesterlist = []
            elif batchid != 'NotAssign' and sem == 'ALL' and batchid != 'allbatch':
                studentsemetsterlist = Student.objects.all()
                studentslist = Student.objects.filter(batch=batchid)
                semesterlist = []
            elif batchid == 'NotAssign' and sem == 'ALL':
                studentsemetsterlist = Student.objects.all()
                studentslist = Student.objects.filter(batch=None)
                semesterlist = []
            elif batchid == 'allbatch' and sem == 'ALL':
                studentsemetsterlist = Student.objects.all()
                studentslist = Student.objects.all()
                semesterlist = []
            for student in studentsemetsterlist:
                if student.semester not in semesterlist:
                    semesterlist.append(student.semester)
            batches = Batch.objects.all()
            if batchid != 'NotAssign':
                instance = Batch.objects.get(id=batchid)
                batchid = instance.batchname
            else:
                batchid = "NOT ASSIGN BATCH"
            return render(request,"Instructor/InstuructorStudentFilter.html",{'Students':studentslist,'curinstructor':instructor,'batches':batches,'semesterlist':semesterlist,'semestercur':sem,'batchcur':batchid})
        except:
            return redirect('/InstructorStudentPage')
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")



def InstructorDeleteBatch(request,id):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        obj = get_object_or_404(Batch,id=id)
        obj.delete()
        messages.info(request,'Batch Deleted Successfully')
        return redirect('/InstructorBatch')
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorStudentFilterBatchCreate(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        try:
            sem = request.POST['semester']
            if sem != 'ALL':
                studentsemetsterlist = Student.objects.all()
                studentslist = Student.objects.filter(semester=sem)
                print(studentslist)
                semesterlist = []
                courses = Course.objects.all()
                for student in studentsemetsterlist:
                    if student.semester not in semesterlist:
                        semesterlist.append(student.semester)
                batches = Batch.objects.all()
            else:
                studentsemetsterlist = Student.objects.all()
                studentslist = Student.objects.filter()
                print(studentslist)
                semesterlist = []
                courses = Course.objects.all()
                for student in studentsemetsterlist:
                    if student.semester not in semesterlist:
                        semesterlist.append(student.semester)
                batches = Batch.objects.all()
            return render(request,"Instructor/InstructorBatchCreate.html",{'Students':studentslist,'curinstructor':instructor,'semesterlist':semesterlist,'semester':sem,'courses':courses})
        except:
            return redirect('/InstructorCreateBatch')
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorStudentFilterBatchEdit(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        try:
            id = request.session['batchid'] 
            batch = Batch.objects.get(id=id)
            sem = request.POST['semester']
            if sem != 'ALL':
                studentsemetsterlist = Student.objects.all()
                studentslist = Student.objects.filter(semester=sem)
                print(studentslist)
                semesterlist = []
                courses = Course.objects.all()
                for student in studentsemetsterlist:
                    if student.semester not in semesterlist:
                        semesterlist.append(student.semester)
                batches = Batch.objects.all()
                instructors = Instructor.objects.all()
            else:
                studentsemetsterlist = Student.objects.all()
                studentslist = Student.objects.filter()
                print(studentslist)
                semesterlist = []
                courses = Course.objects.all()
                for student in studentsemetsterlist:
                    if student.semester not in semesterlist:
                        semesterlist.append(student.semester)
                batches = Batch.objects.all()
                instructors = Instructor.objects.all()

            return render(request,"Instructor/InstructorBatchEdit.html",{'batch':batch,'instructors':instructors,'Students':studentslist,'curinstructor':instructor,'semesterlist':semesterlist,'semester':sem,'courses':courses})
        except:
            return redirect('/InstructorBatch')
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")


def InstructorBatchShow(request,id):
    if 'username' in request.session:
        email = request.session['username']
        request.session['batchviewid'] = id
        instructor = Instructor.objects.get(email=email)
        return redirect("/InstuctorBatchShowPage")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")
    return redirect("/InstuctorBatchShowPage")

def InstuctorBatchShowPage(request):
    if 'username' in request.session:
        email = request.session['username']
        if 'batchviewid' in request.session:
            id = request.session['batchviewid'] 
            instructor = Instructor.objects.get(email=email)
            batch = Batch.objects.get(id=id)
            studentcount = Student.objects.filter(batch_id__pk=id).count
            context ={
                'batch':batch,
                'studentcount':studentcount
            }
            return render(request,"Instructor/InstructorBatchView.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def StudentBatch(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            student = Student.objects.get(email=email)
            context ={
                'student':student
            }
            return render(request,"Student/StudentBatch.html",context)
        except:
            messages.info(request,'Password or Username Wrong')
            return redirect("/login")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")

def InstructorSelectedStudentDeleted(request):
    if 'username' in request.session:
        email = request.session['username']
        deletestudentidlist = request.POST.getlist('deletestudent[]')
        if len(deletestudentidlist) == 0:
            messages.info(request,'No Student Selected for deletetion')
            return redirect("/InstructorStudentPage")
        for studentid in deletestudentidlist:
            student = Student.objects.get(id=studentid)
            student.delete()
        messages.info(request,'Selected Student Record Deleted')
        return redirect("/InstructorStudentPage")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")
    
def InstructorCreateNewTopic(request):
    if 'username' in request.session:
        email = request.session['username']
        if 'instructorcourseid' in request.session:
            id = request.session['instructorcourseid'] 
            course = Course.objects.get(id=id) 
            context = {
                'course':course,
            }
            return render(request,'Instructor/InstructorTopicCreate.html',context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorSubmitNewTopic(request):
    if 'username' in request.session:
        email = request.session['username']
        courseid = request.POST['courseid']
        topicname = request.POST['topicname']
        description = request.POST['des']
        course = Course.objects.get(id=courseid)
        topic = Topic.objects.create(course=course,name=topicname,discription=description)
        msg = topicname+' Created Successfully'
        messages.info(request,msg)
        return redirect("/ShowInstructorCourseDetails")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorTopicView(request,id):
    if 'username' in request.session:
        email = request.session['username']
        try:
            topic =Topic.objects.get(id=id)
            context = {
                'topic':topic
            }
            return render(request,'Instructor/InstructorTopicView.html',context)
        except:
            return redirect('/InstructorCourse')
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorTopicEdit(request,id):
    if 'username' in request.session:
        email = request.session['username']
        try:
            topic =Topic.objects.get(id=id)
            context = {
                'topic':topic
            }
            return render(request,'Instructor/InstructorTopicEdit.html',context)
        except:
            return redirect('/InstructorCourse')
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorSubmitEditTopic(request):
    if 'username' in request.session:
        email = request.session['username']
        topicid = request.POST['topicid']
        topicname = request.POST['topicname']
        des = request.POST['des']
        topic = Topic.objects.get(id=topicid)
        topic.name = topicname
        topic.discription = des
        topic.save()
        urlpage = '/ShowInstructorCourseDetails'
        msg =topicname+" Updated successfully"
        messages.info(request,msg)
        return redirect(urlpage)
       
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstuctorDeleteTopic(request,id):
    if 'username' in request.session:
        topic = Topic.objects.get(id=id)
        urlpage = '/ShowInstructorCourseDetails'
        msg =topic.name+" Deleted successfully"
        messages.info(request,msg)
        topic.delete()
        return redirect(urlpage)
       
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InsturctorSelectedTopicDelete(request):
    if 'username' in request.session:
        topicidlist = request.POST.getlist('deletetopic[]')
        if len(topicidlist) == 0:
            messages.info(request,"No topic is selected for deletion")
            urlpage = '/ShowInstructorCourseDetails'
            return redirect(urlpage)
        for topicid in topicidlist:
            topic = Topic.objects.get(id=topicid)
            msg =topic.name+" Deleted successfully"
            messages.info(request,msg)
            topic.delete()
        urlpage = '/ShowInstructorCourseDetails'
        return redirect(urlpage)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")


def StudentTopicView(request,id):
    if 'email' in request.session:
        try:
            email = request.session['email']
            student = Student.objects.get(email=email)
            topic = Topic.objects.get(id = id) 
            context = {
                'topic':topic,
            }
            return render(request,"Student/StudentTopicView.html",context)
        except: 
            return redirect("/StudentCourse")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")

def InstructorCSVDownloadView(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        msg = ""
        batches = Batch.objects.all()
        messages.info(request,msg)
        context = {
             'curinstructor':instructor,
             'batches':batches,
        }
        return render(request,"Instructor/InstucructorCSVDownloadView.html",context)
       
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")


def InstructorDownloadCSV(request):
    if 'username' in request.session:
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        batchid = request.POST['batch']
        if batchid != 'NotAssign' and batchid != 'ALL':
            studentslist = Student.objects.filter(batch=batchid)
            for student in studentslist:
                sem = student.semester
                break
            batch = Batch.objects.get(id=batchid)
            filename = batch.batchname+'_sem_'+str(sem)+'_.csv'
        elif batchid == 'NotAssign':
            studentslist = Student.objects.filter(batch=None)
            filename = 'Batch Not assign_'+'_.csv'
        elif batchid == 'ALL':
            studentslist = Student.objects.all()
            filename = 'ALL STUDENT'+'_.csv'
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename='+filename
            writer = csv.writer(response,delimiter=',')
            writer.writerow(['studentname','city','email','contact','semester','Batch Name','branch','password','address'])
            for obj in studentslist:
                writer.writerow([obj.studentname,obj.city,obj.email,obj.contact,obj.semester,obj.batch,obj.branch,obj.password,obj.address]) 
            return response

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response,delimiter=',')
        writer.writerow(['studentname','city','email','contact','branch','password','address'])
        for obj in studentslist:
            writer.writerow([obj.studentname,obj.city,obj.email,obj.contact,obj.branch,obj.password,obj.address]) 
        return response
       
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")


def StudentAssignmentDetails(request,id):
    if 'email' in request.session:
        email = request.session['email']
        student = Student.objects.get(email=email)
        topic = Topic.objects.get(id=id) 
        assignment = Assignment.objects.filter(student=student,topic_id__pk=id)
        print(assignment)
        context = {
            'topic':topic,
            'assignments':assignment,
        }
        return render(request,"Student/StudentAssignmentDetails.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")

def StudentAssignmentView(request,id):
    if 'email' in request.session:
       
        email = request.session['email']
        request.session['aidview'] = id
        student = Student.objects.get(email=email)
        assignment = Assignment.objects.get(id=id)
        try:
            print('grade before')
            gradeobj = Grade.objects.get(assignment_id__pk=assignment.id,student_id__pk=student.id)
            print('grade after')
            testcases = TestcaseOutput.objects.filter(student_id__pk=student.id,assignment_id__pk=assignment.id)
            print('after testcase')
            context = {
                'assignment':gradeobj.assignment,
                'solution':gradeobj.solution,
                'testcases':testcases,
                'gradeobj':gradeobj,
            }
            return render(request,"Student/StudentAssignmentViewResult.html",context)
        except:
            try:
                
                listtheme =['eclipse','github','chrome','cloud','twilight','nord_dark','monokai']
                print(assignment)
                testcases = Testcase.objects.filter(assignment_id__pk=assignment.id)
            
                finaltestcaselist = []
                JAVA_CODE = """
                public class Main {
                    public static void main(String[] args) {
                        System.out.println("Farewell cruel world");
                    }
                }
                """
                for testobject in testcases:
                    output = testobject.output
                    finaloutput = output.replace('\\n', '\n')

                    TEST_SET = [
                                {       'language_id': 'java',
                                        'sourcefilename': 'Main.java',
                                        'sourcecode': JAVA_CODE,
                                        'expect': { 'outcome': 15, 
                                                    'stdout': finaloutput,
                                                 }

                                }
                                
                    ]

                    for test in TEST_SET:
                        
                        result = run_test_final(test,request)
                       
                        if 'studentexpectedtouput' in request.session:
                            studentexpectedtouput=request.session['studentexpectedtouput'] 
                            if testobject.testcasetype == 'sample':
                                finaltestcaselist.append(testobject.name)
                                finaltestcaselist.append(testobject.input)
                                finaltestcaselist.append(studentexpectedtouput)
                            del request.session['studentexpectedtouput'] 


                print(finaltestcaselist)
                if request.method == "POST":
                    codesubmit = request.POST['codevalue']
                    print(codesubmit)
                    input = request.POST['input']
                    lang = request.POST['lang']
                    curtheme = request.POST['curtheme']
                    print(curtheme)
                    print(input)
                    if lang == 'java':
                        result_obj = run_test('java', codesubmit, 'Main.java',input)
                        output = display_result(result_obj)
                    elif lang == 'python3':
                        result_obj = run_test('python3', codesubmit, 'Main.py',input)
                        output = display_result(result_obj)
                    elif lang == 'cpp':
                        result_obj = run_test('cpp', codesubmit, 'Main.cpp',input)
                        output = display_result(result_obj)
                    elif lang == 'c':
                        result_obj = run_test('c', codesubmit, 'Main.c',input)
                        output = display_result(result_obj)
                    elif lang == 'octave':
                        result_obj = run_test('octave', codesubmit, 'Main.m',input)
                        output = display_result(result_obj)
                    elif lang == 'php':
                        result_obj = run_test('php', codesubmit, 'Main.php',input)
                        output = display_result(result_obj)
                    elif lang == 'pascle':
                        result_obj = run_test('pascal', codesubmit, 'Main.pass',input)
                        output = display_result(result_obj)
                                      
                    context = {
                        'assignment':assignment,
                        'output':output,
                        'code':codesubmit,
                        'langcur':lang,
                        'input':input,
                        'testcases':finaltestcaselist,
                        'listtheme':listtheme,
                        'curtheme':curtheme,
                    }
                else:
                    try:
                        print('before solution is gatted')
                        solution = Solution.objects.get(assignment_id__pk=assignment.id,student_id__pk=student.id)
                        temp = TemporarySaveAssignmentData.objects.get(assignment=assignment,student=student)
                        if solution.code != "":
                            context = {
                            'tabcount':temp.counttab,
                            'testcases':finaltestcaselist,
                            'assignment':assignment,
                            'code':solution.code,
                            'listtheme':listtheme,
                            }
                        else:
                            print('after solution is gatted')
                            context = {
                                'tabcount':temp.counttab,
                                'testcases':finaltestcaselist,
                                'assignment':assignment,
                                'code':temp.tempcode,
                                'listtheme':listtheme,
                            }
                    except:
                        
                        try:
                            print("before temp is gatted")
                            temp = TemporarySaveAssignmentData.objects.get(assignment=assignment,student=student)
                            print("after temp is gatted")
                            context = {
                                'tabcount':temp.counttab,
                                'langcur':temp.language,
                                'testcases':finaltestcaselist,
                                'assignment':assignment,
                                'code':temp.tempcode,
                                'listtheme':listtheme,
                            }
                        except:
                            languages = assignment.language.all()
                            java = False
                            for lang in languages:
                                if lang.name == 'java':
                                    java = True
                            print(java)
                            context = {
                                'java':java,
                                'testcases':finaltestcaselist,
                                'assignment':assignment,
                                'listtheme':listtheme,
                            }
                return render(request,"Student/StudentAssignmentView.html",context)
                
            except:
                listtheme =['eclipse','github','chrome','cloud','twilight','nord_dark','monokai']
                print(assignment)
                if request.method == "POST":
                    codesubmit = request.POST['codevalue']
                    print(codesubmit)
                    input = request.POST['input']
                    lang = request.POST['lang']
                    curtheme = request.POST['curtheme']
                    print(curtheme)
                    print(input)
                    if lang == 'java':
                        result_obj = run_test('java', codesubmit, 'Main.java',input)
                        output = display_result(result_obj)
                    elif lang == 'python3':
                        result_obj = run_test('python3', codesubmit, 'Main.py',input)
                        output = display_result(result_obj)
                    elif lang == 'cpp':
                        result_obj = run_test('cpp', codesubmit, 'Main.cpp',input)
                        output = display_result(result_obj)
                    elif lang == 'c':
                        result_obj = run_test('c', codesubmit, 'Main.c',input)
                        output = display_result(result_obj)
                    elif lang == 'octave':
                        result_obj = run_test('octave', codesubmit, 'Main.m',input)
                        output = display_result(result_obj)
                    elif lang == 'php':
                        result_obj = run_test('php', codesubmit, 'Main.php',input)
                        output = display_result(result_obj)
                    elif lang == 'pascle':
                        result_obj = run_test('pascal', codesubmit, 'Main.pass',input)
                        output = display_result(result_obj)
                    
                    context = {
                        'assignment':assignment,
                        'output':output,
                        'code':codesubmit,
                        'langcur':lang,
                        'input':input,
                        'listtheme':listtheme,
                        'curtheme':curtheme,
                    }
                else:
                    context = {
                    
                        'assignment':assignment,
                        'listtheme':listtheme,
                    }
                return render(request,"Student/StudentAssignmentView.html",context)
          

    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")



def run_test(language, code, filename,input):
    """Execute the given code in the given language.
       Return the result object.
    """
    if input is None:
        runspec = {
            'language_id': language,
            'sourcefilename': filename,
            'sourcecode': code,
          
        }
    else:
        runspec = {
            'input':input,
            'language_id': language,
            'sourcefilename': filename,
            'sourcecode': code,
            
        }

    resource = '/jobe/index.php/restapi/runs/'
    data = json.dumps({ 'run_spec' : runspec })
    result = {}
    content = ''
    headers = {"Content-type": "application/json; charset=utf-8",
               "Accept": "application/json"}
    try:
        connect = http.client.HTTPConnection(JOBE_SERVER)
        connect.request('POST', resource, data, headers)
        response = connect.getresponse()
        if response.status != 204:
            content = response.read().decode('utf8')
            if content:
                result = json.loads(content)
        connect.close()

    except (HTTPError, ValueError) as e:
        print("\n***************** HTTP ERROR ******************\n")
        if response:
            print(' Response:', response.status, response.reason, content)
        else:
            print(e)
    return result



def display_result(ro):
    '''Display the given result object'''
    if not isinstance(ro, dict) or 'outcome' not in ro:
        print("Bad result object", ro)
        return

    outcomes = {
        0:  'Successful run',
        11: 'Compile error',
        12: 'Runtime error',
        13: 'Time limit exceeded',
        15: 'Successful run',
        17: 'Memory limit exceeded',
        19: 'Illegal system call',
        20: 'Internal error, please report',
        21: 'Server overload'}

    code = ro['outcome']
    print("{}".format(outcomes[code]))
    print()
    if ro['cmpinfo']:
        print("Compiler output:")
        print(ro['cmpinfo'])
        print()
        return ro['cmpinfo']
    else:
        if ro['stdout']:
            print("Output:")
            print(ro['stdout'])
            return ro['stdout']
        else:
            print("No output")
        if ro['stderr']:
            print()
            print("Error output:")
            print(ro['stderr'])
            return ro['stderr']


def StudentfinalSubmitcode(request):
    if 'email' in request.session:
        email = request.session['email']
        student = Student.objects.get(email=email)
        sid = student.id
        if request.method == 'POST':
            assignmentid = request.POST['assignmentid']
            codesubmit = request.POST['finalcode']
            lang = request.POST['finallanguage']
            filename = request.POST['filename']
            language = Language.objects.get(name=lang)
            assignment = Assignment.objects.get(id = assignmentid)
          
            try:
                print("beforr grade")
                gradeobj = Grade.objects.get(assignment_id__pk=assignment.id,student_id__pk=student.id)
                print("after grade")
                testcase = TestcaseOutput.objects.filter(student_id__pk=student.id,assignment_id__pk=assignment.id)
                context = {
                    'assignment':gradeobj.assignment,
                    'solution':gradeobj.solution,
                    'testcases':testcase,
                    'gradeobj':gradeobj,
                }
                return render(request,"Student/StudentAssignmentViewResult.html",context)
            except:

                try:
                    print('try')
                    totalpasstestcase = 0
                    totaltestcase = 0
                    print('solution befor')
                    solution = Solution.objects.get(student_id__pk=sid,assignment_id__pk=assignmentid)
                    print('solution gettted')
                    solution.date = datetime.datetime.now()
                    solution.code = codesubmit
                    solution.language = language
                    print('testcases filter try--------befor')
                    testcases = Testcase.objects.filter(assignment_id__pk=assignmentid)
                    print('testcases filter try--------after')
                    print(lang)
                    print(codesubmit)
                    for testobject in testcases:
                        totaltestcase = totaltestcase +1
                        comment = lang + " running"
                        print('tetcases is going to run')
                        output = testobject.output
                        finaloutput = output.replace('\\n', '\n')
                        
                        TEST_SET = [
                                {
                                        'comment':comment,
                                        'language_id': lang,
                                        'sourcecode': codesubmit,
                                        'input':testobject.input,
                                        'sourcefilename': filename,
                                        'parameters': {'cputime':10},
                                        'expect': { 'outcome': 15, 
                                                    'stdout': finaloutput,
                                                }
                                }
                                
                        ]
                        
                        studentexpectedtouput = ""
                        for test in TEST_SET:
                            print('tetcases to check')
                            result = run_test_final(test,request)
                            status = result
                            print(status)
                                
                            if 'studentexpectedtouput' in request.session:
                                studentexpectedtouput=request.session['studentexpectedtouput'] 
                                del request.session['studentexpectedtouput'] 
                                
                            if 'studentouput' in request.session:
                                studentouput=request.session['studentouput'] 
                                del request.session['studentouput'] 

                            GOOD_TEST = "Test Case is Pass"
                            if status == GOOD_TEST:
                                totalpasstestcase = totalpasstestcase + 1

                            print("test case obj before tryy")
                            testoutput = TestcaseOutput.objects.get(testcase_id__pk=testobject.id,assignment_id__pk=assignmentid,student_id__pk=sid)
                            print("test case obj after tryy")
                            testoutput.studentexpectedoutput = studentexpectedtouput
                            testoutput.studentcodeoutput = studentouput
                            testoutput.status = status
                            testoutput.save()
                    print('before percentage and gared and after for')
                    if totaltestcase != 0:
                        percentage = (totalpasstestcase / totaltestcase) * 100
                    else:
                        percentage = 100
                    solution.percentage = percentage
                    
                    if percentage > 90:
                        solution.autograde = 'A'
                    elif percentage >= 80 and percentage <= 90:
                        solution.autograde = 'B'
                    elif percentage >= 70 and percentage < 80:
                        solution.autograde = 'C'
                    elif percentage >= 60 and percentage < 70:
                        solution.autograde = 'D'
                    else:
                        solution.autograde = 'E'

                    
                    print(solution.autograde)
                    print("before solution.save()")
                    solution.save()
                    print("after solution.save()")
                    print("solution updating for student")
                    try:
                        try:
                            temp = TemporarySaveAssignmentData.objects.get(student_id__pk=sid,assignment_id__pk=assignmentid)
                            testcase = TestcaseOutput.objects.filter(student_id__pk=sid,assignment_id__pk=assignmentid)
                            context={
                                    'tabcount':temp.counttab,
                                    'testcases':testcase,
                                    'assignment':assignment,
                                    'solution':solution,
                            }
                        except:
                            testcase = TestcaseOutput.objects.filter(student_id__pk=sid,assignment_id__pk=assignmentid)
                            context={
                                    'tabcount':0,
                                    'testcases':testcase,
                                    'assignment':assignment,
                                    'solution':solution,
                            }

                    except:
                        try:
                            temp = TemporarySaveAssignmentData.objects.get(student_id__pk=sid,assignment_id__pk=assignmentid)
                            context={
                                    'tabcount':temp.counttab,
                                    'assignment':assignment,
                                    'solution':solution,
                            }
                        except:
                            context={
                                    'tabcount':0,
                                    'assignment':assignment,
                                    'solution':solution,
                            }
                    
                    return render(request,"Student/StudentAssignmentSolutionDetails.html",context)

                except:
                    print('except')
                    totalpasstestcase = 0
                    totaltestcase = 0
                    status = "Submitted Assignment"
                    submission = True
                    percentage = 0
                    batch = Batch.objects.get(id=student.batch.id)
                    solution = Solution.objects.create(student=student,assignment=assignment,language=language,status=status,submission=submission,code=codesubmit,batch=batch,percentage=percentage,autograde='A')
                    testcases = Testcase.objects.filter(assignment_id__pk=assignmentid)
                    totaltestcase = 0
                    print(testcases)
                    print(lang)
                    print(codesubmit)

                    for testobject in testcases:
                        comment = lang + " running"
                        totaltestcase = totaltestcase +1
                        output = testobject.output
                        finaloutput = output.replace('\\n', '\n')
                    
                        TEST_SET = [
                            {
                                    'comment':comment,
                                    'language_id': lang,
                                    'sourcecode': codesubmit,
                                    'input':testobject.input,
                                    'sourcefilename': filename,
                                    'parameters': {'cputime':10},
                                    'expect': { 'outcome': 15, 
                                                'stdout': finaloutput,
                                            }
                            }
                            
                        ]
                    
                        studentexpectedtouput = ""
                        for test in TEST_SET:
                            result = run_test_final(test,request)
                            status = result
                            print(status)
                                
                            if 'studentexpectedtouput' in request.session:
                                studentexpectedtouput=request.session['studentexpectedtouput'] 
                                del request.session['studentexpectedtouput'] 
                                
                            if 'studentouput' in request.session:
                                studentouput=request.session['studentouput'] 
                                del request.session['studentouput'] 
                            testoutput = TestcaseOutput.objects.create(studentexpectedoutput=studentexpectedtouput,assignment=assignment,status=status,testcase=testobject,student=student,studentcodeoutput=studentouput,solution=solution)
                            GOOD_TEST = "Test Case is Pass"
                            if status == GOOD_TEST:
                                totalpasstestcase = totalpasstestcase + 1
                            
                            print("test output is create")
                    if totaltestcase != 0:
                        percentage = (totalpasstestcase / totaltestcase) * 100
                    print(percentage)
                    solution.percentage = percentage
                    
                    if percentage > 90:
                        solution.autograde = 'A'
                    elif percentage >= 80 and percentage <= 90:
                        solution.autograde = 'B'
                    elif percentage >= 70 and percentage < 80:
                        solution.autograde = 'C'
                    elif percentage >= 60 and percentage < 70:
                        solution.autograde = 'D'
                    elif percentage < 60:
                        solution.autograde = 'E'
                    print(solution.autograde)
                   
                    solution.save()
                    print("solution is created")

                    testcase = TestcaseOutput.objects.filter(student_id__pk=sid,assignment_id__pk=assignmentid)
                    try:
                        temp = TemporarySaveAssignmentData.objects.get(student_id__pk=sid,assignment_id__pk=assignmentid)
                        context={
                            'tabcount':temp.counttab,
                                'testcases':testcase,
                                'assignment':assignment,
                                'solution':solution,
                        }
                    except:
                        context={
                            'tabcount':0,
                                'testcases':testcase,
                                'assignment':assignment,
                                'solution':solution,
                        }
                    topic = Topic.objects.get(id=assignment.topic.id)
                    course = Course.objects.get(id=topic.course.id)
                    batch = Batch.objects.get(id=student.batch.id)
                    batchname = batch.batchname
                    semester = str(student.semester)
                    instructor = Instructor.objects.get(id=assignment.instructor.id)
                    email_body = """
                    Course Name: """+course.coursename+"""
                    Topic Name: """+topic.name+"""
                    Assignment Name: """+assignment.name+"""
                    Student Name: """+student.studentname+"""
                    Student email: """+student.email+"""
                    Student semester: """+semester+"""
                    Student Batch: """+batchname+"""

                    Go to Login http://localhost:8000/InstructorLogin"""


                    email_title = "New Assignment Submitted by: " + student.studentname
                    print(email_title)
                    print(email_body)
                    send_mail(email_title, email_body, instructor.email,[instructor.email],fail_silently=False)
                    
                    return render(request,"Student/StudentAssignmentSolutionDetails.html",context)
        else:

            if 'aidview' in request.session:
                id = request.session['aidview']
                pageurl = "/StudentAssignmentView/"+str(id)
                return redirect(pageurl)
    else:

        messages.info(request,'Password or Username Wrong')
        return redirect("/login")

def runspec_from_test(test):
    """Return a runspec corresponding to the given test"""
    runspec = {}
    for key in test:
        if key not in ['comment', 'expect', 'files']:
            runspec[key] = test[key]
    if DEBUGGING:
        runspec['debug'] = True
    return runspec


def run_test_final(test,request):
    '''Execute the given test, checking the output'''

    runspec = runspec_from_test(test)
    # First put any files to the server
    for file_desc in test.get('files', []):
        put_file(file_desc)
        response_code = check_file(file_desc[0])
        if response_code != 204:
            print("******** Put file/check file failed ({}). File not found.****".
                  format(response_code))

    # Prepare the request

    data = json.dumps({ 'run_spec' : runspec })
    response = None
    content = ''

    # Do the request, returning EXCEPTION if it broke
    ok, result = do_http('POST', RUNS_RESOURCE, data)
    if not ok:
        return EXCEPTION

   # If not an exception, check the response is as specified
   
   
    #print(result['stdout'])
    request.session['studentouput']  = result['stdout']
    #print(request.session['studentouput'])
    #print("---------------------")
    #print(test['expect']['stdout'])
    request.session['studentexpectedtouput'] =test['expect']['stdout']
    if is_correct_result(test['expect'], result):
        # if VERBOSE:
        #     display_result_test(test['comment'], result)
        # else:
        #     print(test['comment'] + ' OK')
        return GOOD_TEST
    else:
        # print("\n***************** FAILED TEST ******************\n")
        # print(result)
        # display_result_test(test['comment'], result)
        # print("\n************************************************\n")
        return FAIL_TEST


def do_http(method, resource, data=None):
    """Send the given HTTP request to Jobe, return a pair (ok result) where
       ok is true if no exception was thrown, false otherwise and
       result is a dictionary of the JSON decoded response (or an empty
       dictionary in the case of a 204 response.
       As a special-case hack for testing 400 error conditions, if the
       decoded JSON response is a string (which should only occur when an
       error has occurred), the returned result string is prefixed by the
       response code.
    """
    result = {}
    ok = True
    headers = {"Content-type": "application/json; charset=utf-8",
               "Accept": "application/json"}
    try:
        connect = http_request(method, resource, data, headers)
        response = connect.getresponse()
        if response.status != 204:
            content = response.read().decode('utf8')
            if content:
                result = json.loads(content)
        if isinstance(result, str):
            result = str(response.status) + ': ' + result
        connect.close()

    except (HTTPError, ValueError) as e:
        print("\n***************** HTTP ERROR ******************\n")
        if response:
            print(' Response:', response.status, response.reason, content)
        else:
            print(e)
        ok = False
    return (ok, result)

def http_request(method, resource, data, headers):
    '''Send a request to Jobe with given HTTP method to given resource on
       the currently configured Jobe server and given data and headers.
       Return the connection object. '''
    if USE_API_KEY:
            headers["X-API-KEY"] = API_KEY
    connect = http.client.HTTPConnection(JOBE_SERVER)
    connect.request(method, resource, data, headers)
    return connect

def is_correct_result(expected, got):
    '''True iff every key in the expected outcome exists in the
       actual outcome and the associated values are equal, too'''
    for key in expected:
        if key not in got or expected[key] != got[key]:
            return False
    return True

def trim(s):
    '''Return the string s limited to 10k chars'''
    MAX_LEN = 10000
    if len(s) > MAX_LEN:
        return s[:MAX_LEN] + '... [etc]'
    else:
        return s

def display_result_test(comment, ro):
    '''Display the given result object'''
    print(comment)
    if not isinstance(ro, dict) or 'outcome' not in ro:
        print("Bad result object", ro)
        return

    outcomes = {
        0:  'Successful run',
        11: 'Compile error',
        12: 'Runtime error',
        13: 'Time limit exceeded',
        15: 'Successful run',
        17: 'Memory limit exceeded',
        19: 'Illegal system call',
        20: 'Internal error, please report',
        21: 'Server overload. Excessive parallelism?'}

    code = ro['outcome']
    print("Jobe result: {}".format(outcomes[code]))
    print()
    if ro['cmpinfo']:
        print("Compiler output:")
        print(ro['cmpinfo'])
        print()
    else:
        if ro['stdout']:
            print("Output:")
            print(trim(ro['stdout']))
        else:
            print("No output")
        if ro['stderr']:
            print()
            print("Error output:")
            print(trim(ro['stderr']))

def InstructorAssignmentDetails(request,id):
    if 'username' in request.session:
        topic = Topic.objects.get(id=id)
        email = request.session['username']
        instructor = Instructor.objects.get(email=email)
        assignment = Assignment.objects.filter(instructor=instructor,topic_id__pk=id)
        
        context = {
            'topic':topic,
            'assignments':assignment,
        }

        return render(request,"Instructor/InstructorAssignmentDetails.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")


def InstructorCreateAssignment(request,id):
    if 'username' in request.session:
        topic = Topic.objects.get(id=id)
        email = request.session['username']
        language = Language.objects.all()
        instructor = Instructor.objects.get(email=email)
        batch = Batch.objects.filter(instructor=instructor)
        cname = topic.course
        course = Course.objects.get(coursename=cname)
        print(course)
        context = {
            'topic':topic,
            'languages':language,

        }
        return render(request,"Instructor/InstructorAssignmentCreate.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorSubmitNewAssignment(request):
    if 'username' in request.session:
        topicid = request.POST['topicid']
        assignmentname = request.POST['assignmentname']
        defination = request.POST['defination']
        langidlist = request.POST.getlist('lang[]')
        batchidlist = request.POST.getlist('batchid[]')
        email = request.session['username']
        urlpath = "/InstructorAssignmentDetails/"+topicid
        topic = Topic.objects.get(id=topicid)
        cname = topic.course
        course = Course.objects.get(coursename=cname)
        instructor = Instructor.objects.get(email=email)
        batches = Batch.objects.filter(instructor=instructor)

        assignment = Assignment.objects.create(name=assignmentname,defination=defination,instructor=instructor,topic=topic)
        
        for langid in langidlist:
            language = Language.objects.get(id=langid)
            assignment.language.add(language)

        batchlist = []
        for batch in batches:
            studentlist = Student.objects.filter(batch_id__pk=batch.id,course=course)
            for student in studentlist:
                email = student.email
                print(email)
                topic = Topic.objects.get(id=assignment.topic.id)
                course = Course.objects.get(id=topic.course.id)
                message = "Please Submit Assignment on time"
                email_body = """
                Course Name: """+course.coursename+"""
                Topic Name: """+topic.name+"""
                Assignment Name: """+assignment.name+"""

                message:"""+message+"""

                Go to Login http://localhost:8000/login"""
                email_title = "New announcement: " + assignment.name
                print(email_title)
                print(email_body)
                send_mail(email_title, email_body, email,[email],fail_silently=False)
                assignment.student.add(student)
                batch = student.batch 
                assignmentbatch = Batch.objects.get(id = batch.id)
                if assignmentbatch not in batchlist:
                    batchlist.append(assignmentbatch)
                    print(assignmentbatch)
                    assignment.batch.add(assignmentbatch)


        testcasechoices = request.POST.getlist('testcasechoice')
        print(testcasechoices)
        testnames = request.POST.getlist('testname')
        print(testnames)
        testinputs = request.POST.getlist('testinput')
        print(testinputs)
        testoutputs = request.POST.getlist('testoutput')
        print(testoutputs)
        
        for index in range(0,len(testcasechoices)):
            print(index)
            print(testcasechoices[index])
            print(testnames[index])
            print(testinputs[index])
            print(testoutputs[index])
            if testnames[index] != "" and testinputs[index] != "" and testoutputs[index] != "":
                testcase = Testcase.objects.create(name=testnames[index],input=testinputs[index],output=testoutputs[index],assignment=assignment,testcasetype=testcasechoices[index])
        msg = assignmentname + " new Assignment Created successfully"
        messages.info(request,msg)
        return redirect(urlpath)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorAssignmentEdit(request,aid,tid):
    if 'username' in request.session:
        topic = Topic.objects.get(id=tid)
        assignment = Assignment.objects.get(id=aid)
        email = request.session['username']
        language = Language.objects.all()
        instructor = Instructor.objects.get(email=email)
        batch = Batch.objects.filter(instructor=instructor)
        
        try:
            testcases = Testcase.objects.filter(assignment_id__pk=aid)
            context = {
            'assignment':assignment,
            'topic':topic,
            'languages':language,
            'batches':batch,
            'testcases':testcases,
            }
        except:
            context = {
            'assignment':assignment,
            'topic':topic,
            'languages':language,
            'batches':batch,
            }
        return render(request,"Instructor/InstructorAssignmentEdit.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorSubmitEditAssignment(request):
    if 'username' in request.session:
        assignmentid = request.POST['assignmentid']
        topicid = request.POST['topicid']
        assignmentname = request.POST['assignmentname']
        defination = request.POST['defination']
        langidlist = request.POST.getlist('lang[]')
        email = request.session['username']
        urlpath = "/InstructorAssignmentDetails/"+topicid
        topic = Topic.objects.get(id=topicid)
        cname = topic.course
        course = Course.objects.get(coursename=cname)

        instructor = Instructor.objects.get(email=email)
        batches = Batch.objects.filter(instructor=instructor)

        assignment = Assignment.objects.get(id=assignmentid)
        assignment.date = datetime.datetime.now()
        assignment.name = assignmentname
        assignment.defination = defination

        assignment.language.clear()
        for langid in langidlist:
            language = Language.objects.get(id=langid)
            assignment.language.add(language)

        assignment.batch.clear()
        assignment.student.clear()
        batchlist = []
        for batch in batches:
            studentlist = Student.objects.filter(batch_id__pk=batch.id,course=course)
            for student in studentlist:
                print(student)
                email = student.email
                print(email)
                topic = Topic.objects.get(id=assignment.topic.id)
                course = Course.objects.get(id=topic.course.id)
                message = """
                Here are some changes on assignment please check
                Please Submit Assignment on time
                """
                email_body = """
                Course Name: """+course.coursename+"""
                Topic Name: """+topic.name+"""
                Assignment Name: """+assignment.name+"""

                message:"""+message+"""

                Go to Login http://localhost:8000/login"""
                email_title = "New announcement changes in:"+assignment.name
                print(email_title)
                print(email_body)
                send_mail(email_title, email_body, email,[email],fail_silently=False)
                assignment.student.add(student)
                batch = student.batch 
                assignmentbatch = Batch.objects.get(id = batch.id)
                if assignmentbatch not in batchlist:
                    batchlist.append(assignmentbatch)
                    print(assignmentbatch)
                    assignment.batch.add(assignmentbatch)
               
        assignment.save()

        testcasechoices = request.POST.getlist('testcasechoice')
        print(testcasechoices)
        testnames = request.POST.getlist('testname')
        print(testnames)
        testinputs = request.POST.getlist('testinput')
        print(testinputs)
        testoutputs = request.POST.getlist('testoutput')
        testids = request.POST.getlist('testid')
        for index in range(0,len(testcasechoices)):
            print(index)
            print(testcasechoices[index])
            print(testnames[index])
            print(testinputs[index])
            print(testoutputs[index])
            
            try:
                testcase = Testcase.objects.get(id=testids[index])
                testcase.name = testnames[index]
                testcase.input = testinputs[index]
                testcase.output = testoutputs[index]
                testcase.testcasetype = testcasechoices[index]
                testcase.save()
            except:
                if testnames[index]!="" and testoutputs[index]!="" and testinputs[index] != "":
                    testcase = Testcase.objects.create(name=testnames[index],input=testinputs[index],output=testoutputs[index],assignment=assignment,testcasetype=testcasechoices[index])
        msg = assignmentname + " Assignment Updated successfully"
        messages.info(request,msg)
        return redirect(urlpath)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")
 
def InstructorDeleteAssignment(request,aid,tid):
    if 'username' in request.session:
        assignment = Assignment.objects.get(id=aid)
        msg = assignment.name + " Assignment Deleted successfully"
        assignment.delete()
        messages.info(request,msg)
        urlpath = "/InstructorAssignmentDetails/"+tid
        return redirect(urlpath)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorSelectedAssignmentDelete(request):
    if 'username' in request.session:
        topicid = request.POST['topicid']
        urlpath = "/InstructorAssignmentDetails/"+topicid
        assignmentidlist = request.POST.getlist('deleteassignment[]')
        if len(assignmentidlist) == 0:
            msg = "No Assignment Selected for Deletion"
            messages.info(request,msg)
            return redirect(urlpath)
        for aid in assignmentidlist:
            assignment = Assignment.objects.get(id=aid)
            msg = assignment.name + " Assignment Deleted successfully"
            assignment.delete()
            messages.info(request,msg)
        return redirect(urlpath)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorAssignmentView(request,aid,tid):
    if 'username' in request.session:
        topic = Topic.objects.get(id=tid)
        assignment = Assignment.objects.get(id=aid)
        studentcount = assignment.student.count()
        context = {
            'assignment':assignment,
            'topic':topic,
            'studentcount':studentcount,
        }
        return render(request,"Instructor/InstructorAssignmentView.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorTestCaseDetails(request,aid):
    if 'username' in request.session:
        assignment = Assignment.objects.get(id=aid)
        testcases = Testcase.objects.filter(assignment_id__pk=aid)
        topic = assignment.topic
        context = {
            'assignment':assignment,
            'testcases':testcases,
            'coursename':topic.course,
        }
        return render(request,"Instructor/InstructorTestCaseDetails.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorCreateTestcase(request,aid):
    if 'username' in request.session:
        assignment = Assignment.objects.get(id=aid)
        topic = assignment.topic
        context = {
            'assignment':assignment,
            'coursename':topic.course,
        }
        return render(request,"Instructor/InstructorTestCaseCreate.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorSubmitNewTestcase(request):
    if 'username' in request.session:
        if request.method == "POST":
            aid = request.POST['assignmentid']
            testname = request.POST['testcasename']
            testinput = request.POST['testcaseinput']
            testoutput = request.POST['testcaseoutput']
            assignment = Assignment.objects.get(id=aid)
            testcases = Testcase.objects.filter(assignment_id__pk=aid)
            topic = assignment.topic
            testcase = Testcase.objects.create(name=testname,input=testinput,output=testoutput,assignment=assignment)
            msg = testname+" Test Case is Created successfully"
            messages.info(request,msg)
            context = {
                'assignment':assignment,
                'testcases':testcases,
                'coursename':topic.course,
             }
            return render(request,"Instructor/InstructorTestCaseDetails.html",context)
        else:
            return redirect("/InstructorCourse")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorTestcaseEdit(request,tid,aid):
    if 'username' in request.session:
        assignment = Assignment.objects.get(id=aid)
        topic = assignment.topic
        testcase = Testcase.objects.get(id=tid)
        context = {
            'test':testcase,
            'assignment':assignment,
            'coursename':topic.course,
        }
        return render(request,"Instructor/InstructorTestCaseEdit.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorSubmitEditTestcase(request):
    if 'username' in request.session:
        if request.method == "POST":
            aid = request.POST['assignmentid']
            testid = request.POST['testcaseid']
            testname = request.POST['testcasename']
            testinput = request.POST['testcaseinput']
            testoutput = request.POST['testcaseoutput']
            testtype = request.POST['testcasechoice']

            assignment = Assignment.objects.get(id=aid)
            testcases = Testcase.objects.filter(assignment_id__pk=aid)
            topic = assignment.topic
            testcase = Testcase.objects.get(id = testid)
            testcase.name = testname
            testcase.input = testinput
            testcase.output = testoutput
            testcase.testcasetype = testtype
            testcase.save()
            msg = testname+" Test Case is Edited successfully"
            messages.info(request,msg)
            context = {
                'assignment':assignment,
                'testcases':testcases,
                'coursename':topic.course,
             }
            urlpage = "/InstructorTestCaseDetails/"+aid
            return redirect(urlpage)
        else:
            return redirect("/InstructorCourse")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorDeleteTestcase(request,tid,aid):
    if 'username' in request.session:
        assignment = Assignment.objects.get(id=aid)
        testcase = Testcase.objects.get(id=tid)
        msg = testcase.name+" Test Case is Deleted successfully"
        testcase.delete()
        messages.info(request,msg)
        urlpage = "/InstructorTestCaseDetails/"+aid
        return redirect(urlpage)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def DeleteAllSelectedTestcase(request):
    if 'username' in request.session:
        aid = request.POST['assignmentid']
        testcaseidlist = request.POST.getlist('deletetestcase[]')
        if len(testcaseidlist) == 0:
            messages.info(request,'No Test Case Selected for deletetion')
            urlpage = "/InstructorTestCaseDetails/"+aid
            return redirect(urlpage)
        assignment = Assignment.objects.get(id=aid)
        for testid in testcaseidlist:
            testcase = Testcase.objects.get(id = testid)
            msg = testcase.name +" Test Case is Deleted successfully"
            messages.info(request,msg)
            testcase.delete()
        urlpage = "/InstructorTestCaseDetails/"+aid
        return redirect(urlpage)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorStudentAssignmentDetails(request,aid):
    if 'username' in request.session:
        if request.method == "POST":
            batchid = request.POST['batch']
            if batchid != "ALL":
                batch = Batch.objects.get(id = batchid)
                assignment = Assignment.objects.get(id=aid)
                totalstudent = 0
                students = Student.objects.filter(batch_id__pk=batchid)
                solutions = Solution.objects.filter(assignment_id__pk=aid,batch_id__pk=batchid)
                submitsudentcount = 0
                finallistnotsubmitted = []
                for student in students:
                    totalstudent += 1
                    finallistnotsubmitted.append(student)

                for solution in solutions:
                    cursolutiontudent = solution.student
                    if cursolutiontudent in finallistnotsubmitted:
                        submitsudentcount+=1
                        finallistnotsubmitted.remove(cursolutiontudent)
              
                context = {
                    'submitsudentcount':submitsudentcount,
                    'totalstudent':totalstudent,
                    'curbatch':batch.batchname,
                    'students':finallistnotsubmitted,
                    'solutions':solutions,
                    'assignment':assignment,
                    
                }
            else:
                assignment = Assignment.objects.get(id=aid)
                totalstudent = assignment.student.count
                students = assignment.student.all()
                solutions = Solution.objects.filter(assignment_id__pk=aid)
                submitsudentcount = 0
                finallistnotsubmitted = []
                for student in students:
                    finallistnotsubmitted.append(student)

                for solution in solutions:
                    cursolutiontudent = solution.student
                    if cursolutiontudent in finallistnotsubmitted:
                        submitsudentcount+=1
                        finallistnotsubmitted.remove(cursolutiontudent)
                context = {
                    'submitsudentcount':submitsudentcount,
                    'totalstudent':totalstudent,
                    'curbatch':'ALL',
                    'students':finallistnotsubmitted,
                    'solutions':solutions,
                    'assignment':assignment,
                    
                }
        else:
            assignment = Assignment.objects.get(id=aid)
            totalstudent = assignment.student.count()
            students = assignment.student.all()
            solutions = Solution.objects.filter(assignment_id__pk=aid)
            submitsudentcount = 0
            finallistnotsubmitted = []
            for student in students:
                finallistnotsubmitted.append(student)

            for solution in solutions:
                cursolutiontudent = solution.student
                if cursolutiontudent in finallistnotsubmitted:
                    submitsudentcount+=1
                    finallistnotsubmitted.remove(cursolutiontudent)
            context = {
                'submitsudentcount':submitsudentcount,
                'totalstudent':totalstudent,
                'students':finallistnotsubmitted,
                'solutions':solutions,
                'assignment':assignment,
                
            }
        return render(request,"Instructor/InstructorStudentAssignmentDetails.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def InstructorStudentSolutionView(request,slid):
    if 'username' in request.session:
        solution = Solution.objects.get(id=slid)
        sid  = solution.student.id
        aid = solution.assignment.id
        testcase = TestcaseOutput.objects.filter(student_id__pk=sid,assignment_id__pk=aid)
        temp = TemporarySaveAssignmentData.objects.get(student_id__pk=sid,assignment_id__pk=aid)
        try:
            gradeobj = Grade.objects.get(student_id__pk=sid,assignment_id__pk=aid)
            context = {
                'opentab':temp.counttab,
                'gradeobj':gradeobj,
                'solution':solution,
                'testcases':testcase,
            }
        except:
            context = {
                'opentab':temp.counttab,
                'solution':solution,
                'testcases':testcase,
            }
        return render(request,"Instructor/InstructorStudentAssignmentCheck.html",context)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")


def GradeSubmit(request):
    if 'username' in request.session:
        if request.method == 'POST':
            studentid = request.POST['studentid']
            solutionid = request.POST['solutionid']
            percentage = request.POST['percentage']
            grade = request.POST['grade']      
            assignmentid = request.POST['assignmentid'] 

            solution = Solution.objects.get(id=solutionid)
            assignment = Assignment.objects.get(id=assignmentid)    
            student = Student.objects.get(id=studentid)
            pageurl = "InstructorStudentSolutionView/"+solutionid
            try:
                gradeobj = Grade.objects.get(student=student,solution=solution,assignment=assignment)
                gradeobj.name = grade
                gradeobj.percentage = percentage
                gradeobj.save()
                msg = "Grade Updated to " + student.studentname
                messages.info(request,msg)
            except:
                gradeobj = Grade.objects.create(name=grade,solution=solution,percentage=percentage,student=student,assignment=assignment)
                msg = "Grade added to " + student.studentname
                messages.info(request,msg)
        return redirect(pageurl)
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/InstructorLogin")

def storeeverysecond(request):
    if 'email' in request.session:
        print()
        print()
        print()
        print("method is called")
        if request.method == "POST":
            #print("1")
            email = request.session['email']
            #print("2")
            student = Student.objects.get(email=email)
            #print("3")
            code = request.POST['tempsave']
            #print("4")
            assignmentid = request.POST['assignmentid']
            #print("5")
            finallanguage = request.POST['curlanguage']
            #print("6")
            countvalue = request.POST['countvalue']
            #print("7")
            assignment = Assignment.objects.get(id=assignmentid)
            #print("8")
            msgassignemt = "Assignment id "+assignmentid
            #print("9")
            #print("all ok")
            print()
            print()
            print(msgassignemt)
            #print("10")
            print()
            print()
            curlanguagemsg = "Current Language "+finallanguage
            #print("11")
            print(curlanguagemsg)
            #print("12")
            print()
            print()
            #print(type(countvalue))
            if countvalue != "":
                #print("13")
                try:
                    #print("14")
                    intcountvalue = int(countvalue)
                    #print("15")
                    #msgcountvalue = "Count Tab "+intcountvalue
                    #print(msgcountvalue)
                except:
                    #print("16")
                    print("exception in covversion")
            #print("17")
            print(code)
            #print("18")
            try:
                #print("19")
                if countvalue != "":
                    #print("20")
                    #print("count value befor ok")
                    temp = TemporarySaveAssignmentData.objects.get(assignment=assignment,student=student)
                    #print("21")
                    #print("count value after ok")
                    #print("22")
                    intcount = temp.counttab
                    #print("23")
                    
                    #print(type(intcount))
                    print()
                    #print("count tab string befor ok")
                    #print("24")
                    msgcountvalue = "Count Tab "+str(intcount)
                    #print("25")
                    #print("count tab string after ok")
                    #print("26")
                    print(msgcountvalue)
                    print()
                    print()
                    #print("28")
                    if intcountvalue != "": 
                        #print("29")
                        #print("inside intcount")
                        if intcountvalue >= intcount:
                            #print("30")
                            #print("inside if condition intcount")
                            temp.counttab = countvalue
                            #print("31")
                            temp.save()
                            #print("32")
                            #print("count updated")
                            #print("33")
                        #print("34")
                    #print("35")
                #print("36")
                if code != "":
                    #print("code befor ok")
                    #print("37")
                    temp = TemporarySaveAssignmentData.objects.get(assignment=assignment,student=student)
                    #print("38")
                    #print("code after ok")
                    temp.tempcode = code
                    #print("39")
                    temp.language = finallanguage
                    #print("40")
                    temp.save()
                    #print("41")
                    #print("all okkkkk no error")
                    print()
                    #print("code updated")
                else:
                    return render(request,"Student/StudentAssignmentView.html")
            except:
                #print("42")
                temp = TemporarySaveAssignmentData.objects.create(assignment=assignment,student=student,tempcode=code,language=finallanguage)
                #print("43")
                print("created")
        print()
        print()
        print()        
        return render(request,"Student/StudentAssignmentView.html")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")

def limitover(request):
    if 'email' in request.session:
        return render(request,"Student/StudentLimit.html")
    else:
        messages.info(request,'Password or Username Wrong')
        return redirect("/login")