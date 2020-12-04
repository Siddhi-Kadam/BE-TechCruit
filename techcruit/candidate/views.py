from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def dashCandidate(request):
    return HttpResponse("Candidate DashBoard")