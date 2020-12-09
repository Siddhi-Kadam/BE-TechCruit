from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def dashCandidate(request):
    # return HttpResponse("Candidate DashBoard")
    username = request.session["user"]
    return render(request, 'candidate/homepage.html', {'username': username})


def profile(request):
    username = request.session["user"]
    return render(request, 'candidate/profile.html', {'username': username})


def resume(request):
    username = request.session["user"]
    return render(request, 'resume/resume.html', {'username': username})

