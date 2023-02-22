from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, LandLordProfile, LandLordPaymentDetails
# from django.contrib.auth.models import User


from payment_manager.bankList import BankList


class LandLordPaymentDetailsform(forms.ModelForm):
    account_name = forms.CharField(max_length=150, required=True, label="Account Name",  
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'placeholder':"First Name Other Name Sur Name"}))
    account_number = forms.IntegerField(required=True, label="Account Number", 
                                        widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder': '0000000000'
                                        }))
    class Meta:
        model = LandLordPaymentDetails 
        exclude = ['user_profile']


class LandLordCreationForm(forms.ModelForm):
    referral_code = forms.CharField(max_length=20, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = LandLordProfile
        fields = ['national_id_number', 'national_id_image', 'profile_photo']
        
        widgets = {
            'national_id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id_image' : forms.FileInput(attrs={'class': 'form-control'}),
            'profile_photo' : forms.FileInput(attrs={'class': 'form-control'}),
        }
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=220, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=200, 
                               widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class":"form-control"}))

class UserForm(UserCreationForm):
    password1 = forms.CharField(max_length=200, label="Password",
                               widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class":"form-control"}))
    password2 = forms.CharField(max_length=200, label="Password confirmation",
                               widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class":"form-control"}))
    
    class Meta:
        model = User
        fields = ['first_name', 'sur_name', 'username', 'email', 'password1', 'password2', 'phone_no']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sur_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={"autocomplete": "new-password",'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
            'phone_no': forms.NumberInput(attrs={'class': 'form-control'}),
        }
            
        
class UserUpdateForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'sur_name', 'username', 'email', 'phone_no']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sur_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),  
            'phone_no': forms.NumberInput(attrs={'class': 'form-control'}),
        }