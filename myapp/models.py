from django.db import models
# Create your models here.
# ORM - Object Relational Mapping

class User(models.Model):
    
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    pic = models.FileField(upload_to='Profile',default='avtar.png')
    address = models.TextField(default=True,null=True)
    def __str__(self):
        return self.email

class Event(models.Model):
    secretary = models.ForeignKey(User,on_delete=models.CASCADE)
    ename = models.CharField(max_length=20)
    edate = models.DateField()
    evenue = models.CharField(max_length=20)
    edes = models.TextField(default=True,null=True)
    def __str__(self):
        return self.secretary.email