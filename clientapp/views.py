from mimetypes import add_type
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from myapp.models import *
from random import choices, randrange
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def clientindex(request):
    count = 0
    owners = 0
    tenants = 0
    flag = False
    mid= Member.objects.all()
    umid = Member.objects.get(email=request.session['email'])
    ad = Ads.objects.all()
    club = Club.objects.all()
    event = Event.objects.all()
    for i in mid:
        count = count+1
        # print(i.residence_type)
        if i.residence_type == 'Owner':
            owners=owners+1
        else:
            tenants=tenants+1
    try:
        if request.method == 'POST':
            book = Club.objects.get(date = request.POST['date'])
            return render(request,'client-index.html',{'count':count,'owners':owners,'tenants':tenants,'umid':umid,'ad':ad,'msg':'Party House has been already booked for the given date','club':club,'event':event})
    except:
        if request.method == 'POST':
            Club.objects.create(
                member = umid,
                date = request.POST['date'],
                purpose = request.POST['purpose'],
            )
    return render(request,'client-index.html',{'count':count,'owners':owners,'tenants':tenants,'umid':umid,'ad':ad,'club':club,'event':event})

def login(request):
    if request.method == 'POST':
        try:
            mid = Member.objects.get(email=request.POST['username'])
            if request.POST['password'] == mid.password:
                request.session['email'] = request.POST['username']
                return redirect('client-index')
            return render(request,'login.html',{'msg':'Pasword is incorrect'})
        except:
            return render(request,'login.html',{'msg':'Acccount does not exists'})
    return render(request,'login.html')

def house_details(request):
    umid = Member.objects.get(email=request.session['email'])
    if request.method == 'POST':
        umid.fname = request.POST['fname']
        umid.lname = request.POST['lname']
        umid.mobile = request.POST['mobile']
        umid.house_no = request.POST['hno']
        umid.lane = request.POST['lane']
        umid.residence_type = request.POST['rtype']
        umid.doc_type = request.POST['dtype']
        umid.doc_id = request.POST['did']
        umid.save()
        return render(request,'my-house-details.html',{'umid':umid,'msg':'Profile has been updated'})
    return render(request,'my-house-details.html',{'umid':umid})

def change_member_password(request):
    umid = Member.objects.get(email=request.session['email'])
    if request.method == 'POST':
        if request.POST['member-current-password'] == umid.password:
            if request.POST['member-new-password'] == request.POST['member-confirm-password']:
                umid.password=request.POST['member-new-password']
                umid.save()
                return redirect('client-index')
            return render(request,'change-member-password.html',{'msg':'Both Password does not match'})
        return render(request,'change-member-password.html',{'msg':'Current Password is invalid'})
    return render(request,'change-member-password.html',{'umid':umid})

def advertise(request):
    umid = Member.objects.get(email=request.session['email'])
    try:
        ad = Ads.objects.get(member = umid)
        return render(request,'advertise.html',{'msg':'You have already placed an Advertisement'})
    except:
        if umid.residence_type == "Owner":
            if request.method == 'POST':
                Ads.objects.create(
                    member = umid,
                    ad_type = request.POST['ad_type'],
                    ad_price = request.POST['ad_price'],
                    ad_des = request.POST['ad_des'],
                    ad_image1 = request.FILES['ad_image1'],
                    ad_image2 = request.FILES['ad_image2'],
                    ad_image3 = request.FILES['ad_image3'],
                    ad_image4 = request.FILES['ad_image4'],
                )
                return redirect('client-index')
        return render(request,'advertise.html')

def ad_details(request,pk):
    umid = Member.objects.get(email=request.session['email'])
    details = Ads.objects.get(id=pk)
    return render(request,'view-ad-details.html',{'details':details,'umid':umid})

    