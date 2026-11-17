from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=80, unique=True)
    specialist = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    positions = models.ManyToManyField(Position)

    def __str__(self):
        return self.name
