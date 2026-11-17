from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Module(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=80)

    def __str__(self):
        return f'{self.code} · {self.name}'

class Student(models.Model):
    firstName = models.CharField('First name', max_length=100)
    lastName = models.CharField('Last name', max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    email = models.EmailField(blank=True)
    enrolmentDate = models.DateTimeField('Enrolment date', default=timezone.now)
    modules = models.ManyToManyField(Module, blank=True)
    image = models.ImageField(upload_to='students/', blank=True)

    def __str__(self):
        return f'{self.firstName} {self.lastName.upper()}'

    class Meta:
        ordering = ['lastName', 'firstName', 'pk']
