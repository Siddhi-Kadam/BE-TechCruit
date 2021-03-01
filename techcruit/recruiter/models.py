from django.db import models

# Create your models here.


class Register(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    jobTitle = models.CharField(max_length=150)
    bond = models.IntegerField()
    percent10 = models.FloatField()
    percent12 = models.FloatField()
    percentGrad = models.FloatField()
    salary = models.BigIntegerField()
    experience = models.CharField(max_length=3)
    max = models.CharField(max_length=150)


class Code(models.Model):
    uid = models.ForeignKey(Register, on_delete=models.CASCADE)
    code = models.CharField(max_length=500, blank=True, null=True)


class Registered(models.Model):
    uid = models.ForeignKey(Register, on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    candidateID = models.BigIntegerField()
    candidateName = models.CharField(max_length=200)
    percent10 = models.FloatField()
    percent12 = models.FloatField()
    percentGrad = models.FloatField()
    exp = models.CharField(max_length=3)
    status = models.CharField(max_length=20)


class SelectedBeforeTest(models.Model):
    uid = models.ForeignKey(Register, on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    candidateID = models.BigIntegerField()
    candidateName = models.CharField(max_length=200)
    percent10 = models.FloatField()
    percent12 = models.FloatField()
    percentGrad = models.FloatField()
    exp = models.CharField(max_length=3)


class TestQuestions(models.Model):
    user = models.CharField(max_length=200)
    question = models.CharField(max_length=2000)
    qa = models.CharField(max_length=2000)
    qb = models.CharField(max_length=2000)
    qc = models.CharField(max_length=2000)
    qd = models.CharField(max_length=2000)
    qAns = models.CharField(max_length=2000)


class TestScores(models.Model):
    user = models.CharField(max_length=200)
    canID = models.BigIntegerField()
    canUser = models.CharField(max_length=200)
    scores = models.IntegerField()
    status = models.CharField(max_length=20)


class BehavioralQuestions(models.Model):
    question = models.CharField(max_length=2000)
    qa = models.CharField(max_length=2000)
    qb = models.CharField(max_length=2000)
    qc = models.CharField(max_length=2000)
    qd = models.CharField(max_length=2000)
    qe = models.CharField(max_length=2000)
    qAns = models.CharField(max_length=2000)


class TestScores2(models.Model):
    user = models.CharField(max_length=200)
    canID = models.BigIntegerField()
    canUser = models.CharField(max_length=200)
    scores = models.IntegerField()
    status = models.CharField(max_length=20)

