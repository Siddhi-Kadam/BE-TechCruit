from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
import pyautogui
from candidate.views import dashCandidate
from recruiter.views import dashRecruiter
# Create your views here.


def login(request):
    # return HttpResponse("Login Page")
    return render(request, 'login/loginpage.html')


def logging(request):
    if request.method == 'POST':
        username = request.POST['username']
        request.session["user"] = username
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            pyautogui.alert("Successfully logged in")
            if username[:5] == 'admin' and password[:5] == 'admin':
                return redirect(dashRecruiter)
            else:
                return redirect(dashCandidate)
        else:
            pyautogui.alert("Wrong Username or Password")
            return redirect('/login')
    else:
        return redirect('/login')


def logout(request):
    auth.logout(request)
    return redirect('/login')
