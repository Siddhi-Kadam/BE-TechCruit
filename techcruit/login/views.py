from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
import pyautogui

# Create your views here.


def login(request):
    # return HttpResponse("Login Page")
    return render(request, 'login/loginpage.html')


def logging(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            pyautogui.alert("Successfully logged in")
            return redirect('/')
        else:
            pyautogui.alert("Wrong Username or Password")
            return redirect('/login')
    else:
        return redirect('/login')
