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

