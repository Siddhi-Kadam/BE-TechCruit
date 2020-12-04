from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def dashRecruiter(request):
    return HttpResponse("Recruiter Dashboard")