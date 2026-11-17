from django.db import models

class Hash(models.Model):
    text = models.TextField()
    hash = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.hash
