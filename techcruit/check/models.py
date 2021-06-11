from django.db import models


# Create your models here.
class Upload(models.Model):
    name = models.CharField(max_length=300)
    resume = models.FileField(upload_to='resumes')
