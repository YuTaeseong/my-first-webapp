from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Site_Name(models.Model) :
    site = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    users = models.ManyToManyField(User)
    detail = models.CharField(max_length=200)

    def __str__(self):
        return self.title