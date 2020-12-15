import pyautogui
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Register, Code


# Create your views here.


def dashRecruiter(request):
    username = request.session["user"]
    return render(request, 'recruiter/homepage.html', {'username': username})


def register(request):
    username = request.session["user"]
    return render(request, 'recruiter/register.html', {'username': username})


def registered(request):
    if request.method == 'POST':

        # Register Info
        name = request.POST.get('name')
        jobTitle = request.POST.get('jobTitle')
        bond = request.POST.get('bond')
        percent10 = request.POST.get('percent10')
        percent12 = request.POST.get('percent12')
        salary = request.POST.get('salary')
        experience = request.POST.get('experience')

        username = request.session["user"]
        try:
            obj = Register.objects.latest('id')
            uid = obj.id + 1
        except Register.DoesNotExist:
            uid = 1

        # Saving in Register Info
        o = Register(id=uid, username=username, name=name, jobTitle=jobTitle, bond=bond,
                     percent10=percent10, percent12=percent12, salary=salary, experience=experience)
        o.save()

        # Code Info
        code = request.POST.get('code')

        # Saving Code Info
        abc = Code(uid_id=uid, code=code)
        abc.save()

    pyautogui.alert("Successfully Registered")
    return redirect('/recruiter/')
