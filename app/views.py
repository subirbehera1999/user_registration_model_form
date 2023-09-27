from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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