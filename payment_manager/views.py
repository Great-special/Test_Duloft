from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import Http404, HttpResponseBadRequest
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Payment
from .forms import MakePaymentForm, PaymentForm

from houses.models import HouseModel, FlatModel, SpaceModel

# Create your views here.

from .auto_transfer import autoTransfer
import requests
import os



def verify_payment(request, ref:str):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Payment verified')
        
    else:
        messages.error(request, 'Payment not verified')
    return redirect('userprofile')


def initiate_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            return render(request, 'make_payment.html', {'data': payment, 'Public_key':settings.PAY_PUBLIC_KEY})
    else:
        form = PaymentForm()

    return render(request, 'initiate_payment.html',{'form': form, })


def create_payment(amount, description, depositor, email, owner, recipient_name, 
                   apartment_paidfor=None, space_paidfor=None, commission=0.00):
    """
        This function creates a payment instance in the data base
    """
    init_pay = Payment.objects.create(
        amount=amount,
        commission=commission,
        depositor=depositor,
        description=description,
        owner=owner,
        email=email,
        apartment_paidfor=apartment_paidfor,
        space_paidfor=space_paidfor,
        recipient_name=recipient_name
    )
    return init_pay


def make_payment(request,  house_id, flat_id):
    pass 


def initiate_payment_maintest(request, house_id, flat_id):
    commission_rate = 0.05
    paid = False
    if request.user.is_authenticated and not request.user.is_landlord:
        try:
            full_name = request.user.first_name + ' ' + request.user.sur_name
        except :
            full_name = request.user
            
        # obj = HouseModel.objects.get(id=2) 
        try:
            flat = FlatModel.objects.filter(house__id=house_id).get(id=flat_id) # getting a single flat from a house in the database
        except ObjectDoesNotExist:
            space = SpaceModel.objects.filter(house__id=house_id).get(id=flat_id)
            
            house = space.house.name
            landlord = space.house.landlord.get_full_name()
            recipient_name = space.house.landlord
            amount = space.price
            commission = float(amount) * commission_rate
            description = f"Payment for an apartment [ {space} ] in {house} by {full_name} to {landlord}"
            
            
            # Checking if this payment is the first payment by user
            queryset = Payment.objects.filter(owner=request.user)
            print(queryset.exists())
            
            if queryset.exists():
                print('Not First')
                
                for query in queryset:
                    print(query)
                    if query.verified:
                        paid = True
                        break
                
                if paid:
                    init_pay = create_payment(amount, description, full_name, 
                                            request.user.email, request.user, recipient_name, others_paidfor=space)
                else:
                    print('Haven\'t paid before')
                    init_pay = create_payment(amount, description, full_name, request.user.email, 
                                            request.user, recipient_name, others_paidfor=space, commission=commission)
            else:
                print('first')
                init_pay = create_payment(amount, description, full_name, request.user.email, 
                                            request.user, recipient_name, others_paidfor=space, commission=commission)
                
            context = {'data': init_pay, 'Public_key':settings.PAY_PUBLIC_KEY}
            print(init_pay.amount, init_pay.description)
            return render(request, 'make_payment.html', context)
        
        else:
            house = flat.house.name
            landlord = flat.house.landlord.get_full_name()
            recipient_name = flat.house.landlord
            amount = flat.price
            commission = float(amount) * commission_rate
            description = f"Payment for an apartment [ {flat} ] in {house} by {full_name} to {landlord}"
            
            
            # Checking if this payment is the first payment by user
            queryset = Payment.objects.filter(owner=request.user)
            print(queryset.exists())
            
            if queryset.exists():
                print('Not First')
                
                for query in queryset:
                    print(query)
                    if query.verified:
                        paid = True
                        break
                
                if paid:
                    init_pay = create_payment(amount, description, full_name, 
                                            request.user.email, request.user, recipient_name, flat,)
                else:
                    print('Haven\'t paid before')
                    init_pay = create_payment(amount, description, full_name, request.user.email, 
                                            request.user, recipient_name, flat, commission=commission)
            else:
                print('first')
                init_pay = create_payment(amount, description, full_name, request.user.email, 
                                            request.user, recipient_name, flat, commission=commission)
                
            context = {'data': init_pay, 'Public_key':settings.PAY_PUBLIC_KEY}
            print(init_pay.amount, init_pay.description)
            return render(request, 'make_payment.html', context)
    elif request.user.is_authenticated and request.user.is_landlord:
        return HttpResponseBadRequest('Invalid request land lords cannot pay rent')
    else:
        return HttpResponseBadRequest('Invalid request login to pay rent')
        
        


    


def make_transfer(request, id):
    pass



autoTransfer()