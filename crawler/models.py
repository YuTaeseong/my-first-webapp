from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Site_Name(models.Model) :
    title = models.CharField(max_length=200)
    users = models.ManyToManyField(User, null=True)

    def __str__(self):
        return self.title

class Data_Base(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(null=True)
    site = models.ForeignKey(Site_Name)

    def __str__(self):
        return self.title

class Data_Digital(Data_Base):
    pass

class Data_SeongSu(Data_Base):
    pass

class Data_Hyunime(Data_Base):
    pass