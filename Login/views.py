from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .models import Profile
from .forms import ProfileForm,SignUpForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
# for show messages :
from django.contrib import messages



# Create your views here.


def signUp(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"account created successfully !")
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
                return HttpResponseRedirect(reverse('Shop:home'))
    #return HttpResponse("Logged in")     
    return render(request,'Login/Login.html',context={"form":form})



@login_required
def logoutUser(request):
    logout(request)
    messages.warning(request,"You are Logged out !!")
    return HttpResponseRedirect(reverse('Shop:home'))



@login_required
def userProfile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileForm(instance = profile)
    if request.method == "POST":
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"profile updated successfully !")
            form = ProfileForm(instance=profile)
    return render(request,'Login/ChangeProfile.html',context={'form':form})