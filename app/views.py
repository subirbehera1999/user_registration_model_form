from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random

# Create your views here.
def user_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def registration(request):
    if request.session.get('username'):
        logout(request)
    USFO=Userform()
    PFO=Profileform()
    d={'USFO':USFO,'PFO':PFO}
    if request.method=="POST" and request.FILES:
        UFDO=Userform(request.POST)
        PFDO=Profileform(request.POST,request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            MUFDO=UFDO.save(commit=False)
            MUFDO.set_password(UFDO.cleaned_data['password'])
            MUFDO.save()

            MPFDO=PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('Registration',
                      'your registration process successful',
                      'subirbehera1999@gmail.com',
                      [MUFDO.email],
                      fail_silently=False)
            
            
            return HttpResponse("registration successful")
    
    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

@login_required
def change_password(request):
    if request.method=="POST":
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(request.POST['password'])
        UO.save()
        logout(request)
        
    return render(request,'change_password.html')
@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)

def forget_password(request):
    if request.method=="POST":
        username=request.POST['username']
        QSU=User.objects.filter(username=username)
        if len(QSU)!=0:
            UO=QSU[0]
            UO.set_password(request.POST['password'])
            UO.save()
            return HttpResponseRedirect(reverse('user_login'))
    return render(request,'forget_password.html')











# def forget_password(request):
#     if request.method=="POST":
#         username=request.POST['username']
#         QSU=User.objects.filter(username=username)
#         if len(QSU)!=0:
#             UO=QSU[0]
#             CODE=random.randint(1000,9999)
#             send_mail('Reset password',
#                       {{CODE}},
#                       'subirbehera1999@gmail.com',
#                       [UO.email],
#                       fail_silently=False)
#             d={'UO':UO,'CODE':CODE}

#             yield render(request,'verification_code.html',d)
#             if request.method=="POST":
#                 if request.POST['vcode']==CODE:


#     return render(request,'forget_password.html')

# def verification_code(request):
#     if request.method=="POST":

#     return render(request,'verification_code.html')