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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.check, name='Eligibility Check Page'),
    path('writeCSV', views.writeCSV, name='Write CSV'),
    path('resumeUpload', views.resumeUpload, name='Upload Resume'),
    path('resumeUploaded', views.resumeUploaded, name='Uploaded Resume'),
    path('evaluate', views.evaluate, name='evaluate'),
    path('resumeAnalysis', views.resumeAnalysis, name='resumeAnalysis'),
    path('resumeScreening', views.resumeScreening, name='resumeScreening'),
    path('mlAnalysis', views.mlAnalysis, name='ML Analysis'),
    path('knn', views.knn, name='KNN'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
