from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# from payment_manager.paystack import PayStack

from .models import User, LandLordProfile, LandLordPaymentDetails
from .forms import UserForm, UserUpdateForm, LoginForm, LandLordCreationForm, LandLordPaymentDetailsform

from houses.models import HouseModel, FlatModel, SpaceModel

from payment_manager.models import Payment
# Paystack = settings.PAYSTACK

# Create your views here.

import requests

url = "https://api.verified.africa/sfx-verify/v3/id-service/"


headers = {
    "accept": "application/json",
    "userid": "1674175381223",
    "apiKey": "KC69ZuFxVEsSpld69koD",
    "content-type": "application/json"
}


true = True

def landlordpaymentdetail(request):
    if request.method == "POST":
        payment_details_form = LandLordPaymentDetailsform(request.POST)
        if payment_details_form.is_valid():
            
            account_number = payment_details_form.cleaned_data["account_number"]
            account_name = payment_details_form.cleaned_data["account_name"]
            bank_name = payment_details_form.cleaned_data["bank_name"]
            user_fullname = request.user.get_full_name()
            user_reversed_name = request.user.get_reversed_name()
            print(user_fullname)
            print(user_reversed_name)
            # status, data = Paystack.verify_account_number(account_number,bank_name)
            # print(status, data)
            # if status:
            #     data_name = data['account_name']
            #     if (account_name.upper() in user_fullname.upper() and user_fullname.upper() in data_name or 
            #         user_reversed_name.upper() in data_name): 
                    
            #         pay = payment_details_form.save(commit=False)
            #         if request.user.is_landlord: 
            #             print('yes !!!')
            #             pay.user_profile = request.user
            #             pay.save()
            #         else:
            #             print('only landlords can add account details')
            #     else:
            #         print('account name and the name on our system must match')
            # else:
            #     print('invaild ')
    else:
        payment_details_form = LandLordPaymentDetailsform()
    
    context = {'payment_details_form': payment_details_form}    
    return render(request, 'add_payment_details.html', context)
            
            
def userdetailsView(request):

    user_profile = User.objects.get(username=request.user)      
    context = {
        'user_detail': user_profile,
    }
    return render(request, 'page-my-profile.html', context)


def get_buildings_by_landlord(request):
    if request.user.is_landlord:
        buildings = HouseModel.objects.filter(landlord=request.user)
        return render( request, 'page-my-properties.html', {'properties':buildings})

def get_apartment_by_landlord(request):
    if request.user.is_landlord:
        buildings = FlatModel.objects.filter(house__landlord=request.user)
        return render( request, 'my-apartment.html', {'properties':buildings})

def get_space_by_landlord(request):
    if request.user.is_landlord:
        buildings = SpaceModel.objects.filter(house__landlord=request.user)
        return render( request, 'my-spaces.html', {'properties':buildings})


def get_building_for_tenant(request):
    Paid_Accommodations = []
    spaces_paid = Payment.objects.filter(owner=request.user)
    # print(spaces_paid)
    for space in spaces_paid:
        # print(space, 'space')
        if space.verified:
            Paid_Accommodations.append(space.space_paidfor)
    # print(Paid_Accommodations, 'PA')
    context = {
        'paid_accommodation':Paid_Accommodations,
    }
    return render(request, 'page-my-properties.html', context)

def landlordDashboardView(request):
    user_profile = User.objects.get(username=request.user)
    # using reverse relationship to fetch house, payment, transfer/transaction
    buildings = user_profile.housemodel_set.all()
    pending = user_profile.recipient.all()
    received = user_profile.transactiondetail_set.all()
    referrals = user_profile.referrals.all()
    try:
        paymentdetail = user_profile.paymentdetail
    except ObjectDoesNotExist:
        paymentdetail = None
    """
        Using the reference_id to sort the pending payments and received transactions
        onces a transactions has been completed move it to received by removing it from the pending
        list.
    """
    context = {
        'user_detail': user_profile,
        'buildings': buildings,
        'transactions': {
            'pendings': pending,
            'received': received,
        },
        'referrals': referrals,
        'payment_detail': paymentdetail
    }
    return render(request, 'page-dashboard.html', context=context)
    
            

def landlordprofile(request):
 
    if request.method == 'POST':
        
        form = LandLordCreationForm(request.POST, request.FILES) # Working with Images always add request.Files and enctype='multipart/form-data'
        if form.is_valid():
            try:
                ref_code = form.cleaned_data['referral_code']
                ref_pro = LandLordProfile.objects.get(referral_code=ref_code)
            except:
                pass
            
            NIN = form.cleaned_data['national_id_number']
            payload = {
                "searchParameter": NIN,
                "verificationType": "NIN-SEARCH"
            }
            
            response = requests.post(url, json=payload, headers=headers)

            print(response.json())
            pro = form.save(commit=False)
            pro.user_profile = request.user
            try:
                pro.recommended_by = ref_pro.user_profile.user
            except:
                pass
            pro.save()

            return redirect('.')
        
    else:
        form = LandLordCreationForm()
         
    context = {'form': form}
    return render(request, 'add_landlord_profile.html', context)


def update_landlord_profile(request, pk):
    instance = LandLordProfile.objects.get(user_profile__id = pk)
    form = LandLordCreationForm(instance=instance)
    
    if request.method == 'POST':
        form = LandLordCreationForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            
    context = {'form': form}
    return render(request, 'add_landlord_profile.html', context)



       
def register(request, *args, **kwargs):
    try:
        ref_code = str(kwargs.get('ref_code'))
        profile = LandLordProfile.objects.get(referral_code=ref_code)
    except:
        pass
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # Automatically logining in newly register user 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
           
            return redirect('/')
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'page-register.html', context)


def update_view(request, pk):
    user_obj = User.objects.get(pk=pk)
    form = UserUpdateForm(instance=user_obj)
    
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
    
    return render(request, 'edit-user.html', {'form': form})       
            
            
        
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if authenticate(username=username, password=password):
                user = authenticate(username=username, password=password)
                login(request,user)
                
                return redirect('/')
            
            if authenticate(email=username, password=password):
                user = authenticate(email=username, password=password)
                login(request, user)
                
                return redirect('/')
    else:
        form  = LoginForm
             
    context = {
        'form': form,
    }
    
    return render(request, 'page-login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')