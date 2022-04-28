from pickle import TRUE
from tkinter import CASCADE
from django.db import models
from myapp.models import User

# Create your models here.
class Member(models.Model):
    choice = [('Owner','Owner'),('Tenant','Tenant')]
    secretary = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    lane = models.CharField(max_length=50)
    house_no = models.CharField(max_length=10)
    residence_type = models.CharField(max_length=20,choices=choice)
    doc_type = models.CharField(max_length=20,null=True,default=True)
    doc_id = models.CharField(max_length=20,null=True,default=True)
    def __str__(self):
        return self.email

class Ads(models.Model):
    choice = [('Sell','Sell'),('Rent','Rent')]
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    ad_type = models.CharField(max_length=20,choices=choice)
    ad_price = models.CharField(max_length=20)
    ad_des = models.TextField()
    ad_image1 = models.FileField(upload_to='Ads',blank=True)
    ad_image2 = models.FileField(upload_to='Ads',blank=True)
    ad_image3 = models.FileField(upload_to='Ads',blank=True)
    ad_image4 = models.FileField(upload_to='Ads',blank=True)
    def __str__(self):
        return self.member.email
        
class Club(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    purpose = models.CharField(max_length=20)
    date =  models.DateField()
    def __str__(self):
       return self.member.email

class Complaint(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    cdate = models.DateField(null = True)
    subject = models.CharField(max_length=50)
    des = models.TextField()
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.member.email

class Maintenance(models.Model):
    choice = [('January','January'),('February','February'),('March','March'),('April','April'),('May','May'),('June','June'),('July','July'),('August','August'),('September','September'),('October','October'),('November','November'),('December','December')]
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    payment_date = models.DateField()
    month = models.CharField(max_length=20,choices=choice)
    year = models.IntegerField()
    pay_id = models.CharField(max_length=50)
    verify = models.BooleanField(default=False)
    def __str__(self):
        return self.member.email