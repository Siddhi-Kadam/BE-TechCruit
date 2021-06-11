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
    path('', views.dashCandidate, name='Candidate DashBoard'),
    path('dash2', views.dash2, name='Candidate DashBoard 2'),
    path('profile', views.profile, name='Candidate Profile'),
    path('resume', views.resume, name='Resume View'),
    path('profileSaved', views.profileSaved, name='Candidate Profile Saved'),
    path('bot', views.bot, name='Resume View'),
    path('edit_profile', views.edit_profile, name='Edit Profile'),
    path('editProfileSaved', views.editProfileSaved, name='Edit Profile Saved'),
    path('test1/<int:id>', views.test1, name='Conduct Test 1'),
    path('test2/<int:id>', views.test2, name='Conduct Test 2'),
    path('test1Scores', views.test1Scores, name='Scoring Test 1'),
    path('test2Scores', views.test2Scores, name='Scoring Test 2'),
    path('selection', views.selection, name='Company Selection'),
    path('hackerRank', views.hackerRank, name='HackerRank Certifications'),
    path('hackSaved', views.hackSaved, name='HackerRank Certifications Saved'),

]
