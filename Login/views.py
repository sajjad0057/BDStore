from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .models import Profile
from .forms import ProfileForm,SignUpForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout



# Create your views here.


def signUp(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Login:login'))
    return render(request,'Login/SignUp.html',context={'form':form})


def loginUser(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print("username--->",username)
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponse("Logged in")
    #return HttpResponse("Logged in")       
    return render(request,'Login/Login.html',context={"form":form})