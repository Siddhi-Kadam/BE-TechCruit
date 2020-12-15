from django.db import models

# Create your models here.


class Register(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    jobTitle = models.CharField(max_length=150)
    bond = models.IntegerField()
    percent10 = models.FloatField()
    percent12 = models.FloatField()
    salary = models.BigIntegerField()
    experience = models.CharField(max_length=3)


class Code(models.Model):
    uid = models.ForeignKey(Register, on_delete=models.CASCADE)
    code = models.CharField(max_length=500, blank=True, null=True)
