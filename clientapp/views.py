from mimetypes import add_type
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from myapp.models import *
from random import choices, randrange
from django.conf import settings
from django.core.mail import send_mail
from datetime import date, datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.
def clientindex(request):
    count = 0
    owners = 0
    tenants = 0
    mid= Member.objects.all()
    umid = Member.objects.get(email=request.session['email'])
    ad = Ads.objects.all()
    today_date = date.today()
    club = Club.objects.filter(
        date__gte = today_date
    )
    
    event = Event.objects.filter(
        edate__gte = today_date
    )
    complaint = Complaint.objects.all()
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
            return render(request,'client-index.html',{'count':count,'owners':owners,'tenants':tenants,'umid':umid,'ad':ad,'msg':'Party House has been already booked for the given date','club':club,'event':event,'complaint':complaint,'date':book.date})
    except:
        if request.method == 'POST':
            Club.objects.create(
                member = umid,
                date = request.POST['date'],
                purpose = request.POST['purpose'],
            )
    return render(request,'client-index.html',{'count':count,'owners':owners,'tenants':tenants,'umid':umid,'ad':ad,'club':club,'event':event,'complaint':complaint})

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

def complaint(request):
    umid = Member.objects.get(email = request.session['email'])
    if request.method == 'POST':
        Complaint.objects.create(
            member = umid,
            cdate = date.today(),
            subject = request.POST['subject'],
            des = request.POST['des'],
        )
    complaint = Complaint.objects.all()
    return render(request,'complaint.html',{'umid':umid,'complaint':complaint})

def member_logout(request):
    del request.session['email']
    return redirect('/')



def maintenance(request):
    umid = Member.objects.get(email = request.session['email'])
    # try:
    maintenance_detail = Maintenance.objects.filter(
        member = umid
    )
    if request.method == 'POST':
        maintenance = Maintenance.objects.create(
            member = umid,
            payment_date = date.today(),
            month = request.POST['month'],
            year = request.POST['year'],
        )
        currency = 'INR'
        amount = 50000  # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = f'paymenthandler/{maintenance.id}'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['umid'] = umid
        context['maintenance_detail'] = maintenance_detail
        context['maintenance'] = maintenance
        return render(request,'proceed-maintenance.html',context=context)
    return render(request,'maintenance.html',{'maintenance_detail':maintenance_detail,'umid':umid})






razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
@csrf_exempt
def paymenthandler(request,pk):
    umid = Member.objects.get(email = request.session['email'])
    # only accept POST request.
    if request.method == "POST":
        try:
            maintenance = Maintenance.objects.get(id=pk)
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            # if result is None:
            amount = 50000  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                maintenance.pay_id = payment_id
                maintenance.verify = True
                maintenance.save()
                maintenance_detail = Maintenance.objects.filter(
                member = umid
                )
                # render success page on successful caputre of payment
                return render(request, 'maintenance.html',{'umid':umid,'maintenance_detail':maintenance_detail,'msg':'Payment Successfully Completed'})
            except:
                maintenance_detail = Maintenance.objects.filter(
                member = umid
                )
                # if there is an error while capturing payment.
                return render(request, 'maintenance.html',{'umid':umid,'maintenance_detail':maintenance_detail,'msg':'Payment Failed. Please try again..'})
        # else:
 
            # if signature verification fails.
            # return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


def proceed_maintenance(request):
    if request.method == 'POST':
        umid = Member.objects.get(email = request.session['email'])
        currency = 'INR'
        amount = 50000  # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = f'paymenthandler/{maintenance.id}'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['umid'] = umid
        return render(request,'proceed-maintenance.html',context=context)
    else:
        return redirect('maintenance')
