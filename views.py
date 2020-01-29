from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader,Context
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import Student
from django.conf import settings
from django.core.mail import send_mail
message_1=["Result of Bachelor or Engineering odd semester now","JUMS registration has began for the academic calender 2019-2020","Review examination portal active","Supplementary examination information will be available soon"]
# Create your views here.
def index(request):
    if request.method=='POST':
        if request.POST['password1']==request.POST['password2']:
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            course=request.POST['course']
            department=request.POST['department']
            email=request.POST['email']
            phone_number=request.POST['phone']
            password=request.POST['password1']
            if not Student.objects.filter(username=username).exists():
                text="Welcome to Jums "+first_name+ " " + last_name+ ". Your user name is your roll number.You will receive furthur updates by mail"
                send_mail('Registration in jums',text,settings.EMAIL_HOST_USER,[email],fail_silently=False,)
                a=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password)
                b=Student()
                b.first_name=first_name
                b.last_name=last_name
                b.username=username
                b.password=password
                b.department=department
                b.course=course
                b.email=email
                b.phone=phone_number
                b.save()
                message="Welcome "+a.first_name
                return render(request,"jums/login.html",{"users":[b],"messages":[message]})
            else:
                messages.info(request,'User already registered')
                return render(request,'jums/index.html')
        else:
            messages.info(request,'Passwords do not match')
            return render(request,"jums/take_to_signup_page.html")
    else:
        context={"messages":message_1}
        return render(request,'jums/index.html',context)

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=str(password))
        if user is not None:
            auth.login(request,user)
            a=Student.objects.get(username=username)
            if a is not None :
                message="Welcome "+user.first_name
                context={"users":[a],"messages":[message]}
                return render(request,'jums/login.html',context)
            else:
                message_1.append("Admin portal is different")
                return render(request,"jums/index.html",{"messages":message_1})
        else:
            message_1.append("Invalid user name or password")

            return render(request,"jums/index.html",{"messages":message_1})
    else:
        return redirect('/')
    
def take_to_signup_page(request):
    return render(request,'jums/take_to_signup_page.html')

def logout(request):
    auth.logout(request)
    #message_1.append("Logged out Successfully")
    return render(request,'jums/index.html',{"messages":message_1})

def forgot_password(request):
    return render(request,'jums/forgot_password.html')

def forgot_password_1(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        phone_number=request.POST['phone']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            a=Student.objects.get(username=username)
            if a is None:
                message_1.append("User not in system")
                return render(request,"jums/index.html",{"messages":message_1})
            else:
                if a.email==email and a.phone==phone_number:
                    u = User.objects.get(username=username)
                    u.set_password(password1)
                    a.password=password1
                    u.save()
                    a.save()
                    message_1.append("Password reset")
                    return render(request,"jums/index.html",{"messages":message_1})                    
                else:
                    message_1.append("Invalid email or phone number")
                    return render(request,"jums/index.html",{"messages":message_1}) 
        else:
            message_1.append("Passwords do not match")
            return render(request,"jums/fotgot_password.html",{"messages":message_1})        
    else:
        return render(request,"jums/index.html",{"messages":message_1})




