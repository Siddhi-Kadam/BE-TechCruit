from django.db import models

# Create your models here.


class PersonalInfo(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=500)
    jobTitle = models.CharField(max_length=150)
    date = models.CharField(max_length=10)
    website = models.CharField(max_length=150)
    aadharNo = models.CharField(max_length=20)
    experience = models.CharField(max_length=3)
    mobile = models.BigIntegerField()
    email = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    intro = models.CharField(max_length=1000)


class Coding(models.Model):
    uid = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    language = models.CharField(max_length=500, blank=True, null=True)


class Projects(models.Model):
    uid = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    proName = models.CharField(max_length=500, blank=True, null=True)
    proService = models.CharField(max_length=500, blank=True, null=True)
    proInfo = models.CharField(max_length=500, blank=True, null=True)


class Jobs(models.Model):
    uid = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    span = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=200, blank=True, null=True)
    agency = models.CharField(max_length=500, blank=True, null=True)
    workedOn = models.CharField(max_length=500, blank=True, null=True)
    workPerformed = models.CharField(max_length=500, blank=True, null=True)


class AcademicInfo(models.Model):
    uid = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    span10 = models.CharField(max_length=10, blank=True, null=True)
    university10 = models.CharField(max_length=200, blank=True, null=True)
    school10 = models.CharField(max_length=500, blank=True, null=True)
    percent10 = models.FloatField()
    span12 = models.CharField(max_length=10, blank=True, null=True)
    university12 = models.CharField(max_length=200, blank=True, null=True)
    college12 = models.CharField(max_length=500, blank=True, null=True)
    percent12 = models.FloatField()
    spanGrad = models.CharField(max_length=10, blank=True, null=True)
    courseGrad = models.CharField(max_length=200, blank=True, null=True)
    schoolGrad = models.CharField(max_length=500, blank=True, null=True)
    percentGrad = models.FloatField()
