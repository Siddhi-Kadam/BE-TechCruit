"""techcruit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashRecruiter, name='Recruiter DashBoard'),
    path('register', views.register, name='Recruiter Register'),
    path('registered', views.registered, name='Recruiter Registered'),
    path('auto_select', views.auto_select, name='Auto Select'),
    path('selected_before_test', views.selected_before_test, name='Selected Candidates Before Test'),
    path('questions', views.questions, name='Test 1 Questions'),
    path('checkResume/<int:id>', views.checkResume, name='Check Resume'),
    path('addQuestions', views.addQuestions, name='Add Questions in Test 1'),
    path('uploadQuestions', views.uploadQuestions, name='Upload Questions in Test 1'),
    path('deleteAllQuestions', views.deleteAllQuestions, name='Delete All Questions in Test 1'),
    path('QuestionAdded', views.QuestionAdded, name='Questions added in Test 1'),
    path('QuestionUploaded', views.QuestionUploaded, name='Questions uploaded in Test 1'),
    path('editQuestions/<int:id>', views.editQuestions, name='Edit Questions in Test 1'),
    path('QuestionEdited', views.QuestionEdited, name='Questions edited in Test 1'),
    path('deleteQuestions/<int:id>', views.deleteQuestions, name='Delete Questions in Test 1'),
    path('scores', views.scores, name='Scores for Test 1'),
    path('questions2', views.questions2, name='Test 2 Questions'),
    path('scores2', views.scores2, name='Scores for Test 2'),
    path('scoring', views.scoring, name='Scores for Test 2'),
]
