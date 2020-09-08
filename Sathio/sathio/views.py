from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login
from django.contrib import auth
from django.contrib.auth import logout
# Create your views here.


def index(request):
    return render(request,'index.html')
def tcondition(request):
    return render(request,'terms-conditions.html')
def privacypolicy(request):
	return render(request,'privacy-policy.html')
@login_required(login_url='/Login')
def home(request):
	return render(request,'homepage.html')
def Login(request):
    if request.method == 'POST':
        username  = request.POST.get('username')
        password  = request.POST.get('password')
        user = authenticate(username = username, password=  password)
        if user:
            if user.is_active:
                login(request,user)
                return render(request, 'homepage.html')
        else:
            return render(request,"invalidlogin.html")
    else:
        return render(request,'login.html')
def Logout(request):
    auth.logout(request)
    return render(request,'login.html')
def allpost(request):
	return render(request,'postlisting.html')
	