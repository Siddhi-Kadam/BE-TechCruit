from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import pyautogui as pu

# Create your views here.


def register(request):
    # return HttpResponse("Register")
    return render(request, 'register/registerpage.html')


def registration(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        re_pass = request.POST['re_pass']
        if password == re_pass:
            if User.objects.filter(username=username).exists():
                pu.alert("Username already exists")
                return redirect('/register')
            else:
                x = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email,
                                             password=password)
                x.save()
                pu.confirm("User Created")
                return redirect('/')
        else:
            pu.confirm("Password & Repeated Password don't Match")
            return redirect('/register')
    else:
        return redirect('/register')
