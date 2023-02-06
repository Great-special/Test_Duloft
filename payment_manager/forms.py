from django import forms
from .models import Payment


class MakePaymentForm(forms.Form):
    card_no = forms.CharField(max_length=50)
    cvv = forms.CharField(max_length=5, widget=forms.PasswordInput(attrs={"autocomplete":"new"}))
    expirydate = forms.CharField(widget=forms.DateInput(attrs={"placeholder":"07/20"}))
    # expiryyear = forms.CharField(max_length=10, widget=forms.DateField())
    
    
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'email')