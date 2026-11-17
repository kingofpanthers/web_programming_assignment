from django.db import models

class Student(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(blank = True)
    enrolmentDate = models.DateTimeField()
    modules = models.ManyToManyField('Module', blank = True)

class Module(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
