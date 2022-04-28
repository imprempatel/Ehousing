import email
from django.http import HttpResponse
from django.shortcuts import redirect, render

from clientapp.views import maintenance
from .models import *
from clientapp.models import *
from random import choices, randrange
from django.conf import settings
from django.core.mail import send_mail
from clientapp.models import *
# Create your views here.

def index(request):
    try:
        count = 0
        owner = 0
        tenant = 0
        mid= Member.objects.all()
        for i in mid:
            count = count+1
            if i.residence_type == 'Owner':
                owner = owner+1
            else:
                tenant = tenant+1
        uid = User.objects.get(email=request.session['email'])
        event = Event.objects.all()
        complaint = Complaint.objects.all()
        return render(request,'index.html',{'uid':uid,'count':count,'owner':owner,'tenant':tenant,'event':event,'complaint':complaint})
    except:
        return render(request,'sign-in.html',{'msg':'Session has expired'})

def sign_in(request):
    if request.method == 'POST':
        # try:
            uid = User.objects.get(email=request.POST['email'])
            if request.POST['password'] == uid.password:
                request.session['email'] = request.POST['email']
                return redirect('index')
            return render(request,'sign-in.html',{'msg':'Pasword is incorrect'})
        # except:
        #     return render(request,'sign-in.html',{'msg':'Acccount does not exists'})
    return render(request,'sign-in.html')

def sign_up(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = 'Email already exist'
            return render(request,'sign-up.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                otp = randrange(1000,9999)
                subject = 'OTP verification'
                message = f'Your OTP to validate your email with ehousing is {otp}. Use your login credentials after this to login and start using the application. This otp is confidential so do not share it with anyone'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                global temp
                temp = {
                    'fname' : request.POST['fname'],
                    'lname' : request.POST['lname'],
                    'email' : request.POST['email'],
                    'mobile' : request.POST['mobile'],
                    'password' : request.POST['password'],
                }
                return render(request,'otp.html',{'msg':'OTP sent on your Email!!','otp':otp})
            return render(request,'sign-up.html',{'msg':'Both are not same'})
    return render(request,'sign-up.html')

def otp(request):
    if request.POST['uotp'] == request.POST['otp']:
        global temp
        User.objects.create(
            fname = temp['fname'],
            lname = temp['lname'],
            email = temp['email'],
            mobile = temp['mobile'],
            password = temp['password'],
        )
        del temp
        return render(request,'sign-in.html',{'msg':'Account Created'})
    return render(request,'otp.html',{'msg':'Invalid OTP','otp':request.POST['otp']})

def logout(request):
    del request.session['email']
    return render(request,'sign-in.html')


def forgot_password(request):
    if request.method == 'POST':
        try:
            uid = User.objects.get(email=request.POST['email'])
            s = 'qweertyuiopasdfghklxcvbnm12345684556$%$#'
            password = ''.join(choices(s,k=8))  
            subject = 'Password Has Been Reset'
            message = f'Your New password is {password}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            uid.password = password
            uid.save()
            return render(request,'forgot-password.html',{'msg':'Ne wpassword sent on your email'})

        except:
            return render(request,'forgot-password.html',{'msg':'Account does not exist'})
    return render(request,'forgot-password.html')

def profile(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        uid.fname = request.POST['fname']
        uid.lname = request.POST['lname']
        uid.mobile = request.POST['mobile']
        uid.address = request.POST['address']
        if 'pic' in request.FILES:
            uid.pic = request.FILES['pic']
        uid.save()
        return render(request,'profile.html',{'uid':uid,'msg':'Profile has been updated'})
    return render(request,'profile.html',{'uid':uid})

def change_password(request):
    uid=User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        if request.POST['cpassword'] == uid.password:
            if request.POST['npassword'] == request.POST['cnpassword']:
                uid.password=request.POST['npassword']
                uid.save()
                return render(request,'index.html',{'msg':'Password is changed'})
            return render(request,'cpassword.html',{'msg':'Both Password does not match'})
        return render(request,'cpassword.html',{'msg':'Current Password is invalid'})
    return render(request,'cpassword.html',{'uid':uid})

def add_member(request):
    uid=User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        s = 'qweertyuiopasdfghklxcvbnm12345684556$%$#'
        temp = ''.join(choices(s,k=8))
        mid = Member.objects.create(
        secretary = uid,
        fname = request.POST['fname'],
        lname = request.POST['lname'],
        mobile = request.POST['mobile'],
        email = request.POST['email'],
        residence_type = request.POST['rtype'],
        lane = request.POST['lane'],
        house_no = request.POST['hno'],
        doc_type = request.POST['dtype'],
        doc_id = request.POST['did'],
        password = temp,
        )
        subject = 'You are now registered with E-Housing system'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email'],]
        message = f'''Congratulations you can use the below mentioned details to login to the E-Housing Website.\n Your Email: {recipient_list} \n Your Password:{temp}'''
        send_mail( subject,message,email_from,recipient_list)
        return render(request,'add-member.html',{'msg':'Member has been added','uid':uid})
    return render(request,'add-member.html',{'uid':uid})

def events(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        Event.objects.create(
            secretary = uid,
            ename = request.POST['ename'],
            edate = request.POST['edate'],
            evenue = request.POST['evenue'],
            edes = request.POST['edes'],
        )
        return render(request,'events.html',{'uid':uid,'msg':'Event has been Added'})
    return render(request,'events.html',{'uid':uid})


def edit_event(request,pk):
    uid = User.objects.get(email = request.session['email'])
    try:
        event = Event.objects.get(id=pk)
        if request.method == 'POST':
            event.ename = request.POST['ename']
            event.edate = request.POST['edate']
            event.evenue = request.POST['evenue']
            event.edes = request.POST['edes']
            event.save()
        return render(request,'edit-event.html',{'event':event,'uid':uid})
    except:
        return redirect('index')

def delete_event(request,pk):
    uid = User.objects.get(email = request.session['email'])
    try:
        Event.objects.get(id=pk).delete()
        return redirect('index')
    except:
        return redirect('index')

def view_complaint(request,pk):
    uid = User.objects.get(email = request.session['email'])
    try:
        complaint = Complaint.objects.get(id=pk)
        return render(request,'view-complaint.html',{'uid':uid,'complaint':complaint})
    except:
        return redirect('index')

def resolve_complaint(request,pk):
    uid = User.objects.get(email = request.session['email'])
    try:
        complaint = Complaint.objects.get(id=pk)
        complaint.status = True
        complaint.save()
        return redirect('index')
    except:
        return redirect('index')

def view_maintenance(request):
    uid = User.objects.get(email = request.session['email'])
    try:
        maintenance = Maintenance.objects.all()
        return render(request,'view-maintenance.html',{'uid':uid,'maintenance':maintenance})
    except:
        return render(request,'view-maintenance.html',{'uid':uid,'maintenance':maintenance})

def search_maintenance(request):
    uid = User.objects.get(email = request.session['email'])
    try:
        if request.method == 'POST':
            search = request.POST['search']
            try:
                member = Maintenance.objects.filter(
                    member__email = search,
                    member__verify = True
                )
                return render(request,'view-maintenance.html',{'uid':uid,'member':member})
            except:
                maintenance = Maintenance.objects.all()
                return render(request,'view-maintenance',{'uid':uid,'maintenance':maintenance,'msg':'No match Found'})
    except:
        return redirect('view-maintenance')