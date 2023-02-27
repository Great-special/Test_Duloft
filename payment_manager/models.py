from django.db import models
from django.utils import timezone
import secrets
import uuid
from django.conf import settings
from django.contrib.auth.hashers import make_password
from users.models import User
from .paystack import PayStack
from houses.models import HouseModel, FlatModel, SpaceModel
# Create your models here.


class Payment(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    commission = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # trans_fee = models.DecimalField(max_digits=8, decimal_places=2)
    ref = models.CharField(max_length=100, unique=True)
    depositor = models.CharField(max_length=100, blank=True, null=True)
    recipient_name = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="recipient")
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='payment')
    description = models.TextField(blank=True, null=True)
    email = models.EmailField()
    apartment_paidfor = models.ForeignKey(FlatModel, on_delete=models.PROTECT, null=True, blank=True)
    others_paidfor = models.ForeignKey(SpaceModel, on_delete=models.PROTECT, null=True, blank=True)
    verified = models.BooleanField(default=False)
    # payment_date = models.DateField(default=timezone.now().date)
    date_created = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"
    
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = 'D-'+ secrets.token_urlsafe(25)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if object_with_similar_ref:
                self.ref = models.UUIDField(default=uuid.uuid4, unique=True)
            else:
                self.ref = ref
        if not self.depositor:
            self.depositor = request.user.first_name + ' ' + request.user.sur_name
            
        if not self.apartment_paidfor and not self.others_paidfor:
            print('You are not allowed to leave it empty')
        super().save(*args, **kwargs)
       
    
    def final_amount(self):
        return float(self.amount) + float(self.commission)
    
    
    def validate_amount(self):
        return (float(self.amount) + float(self.commission)) * 100
    
    def verify_payment(self):
        paystack = PayStack(settings.PAY_SECRET_KEY)
        status, result = paystack.verify_payment(self.ref)
        
        if status:
            if result['amount'] / 100 == (float(self.amount) + float(self.commission)):
                self.verified = True
            else:
                self.verified = False
            self.save()
            
        if self.verified:
            return True
        return False
        
    
class TransactionDetail(models.Model):
    transfer_code = models.CharField(('Transfer Code'), max_length=125, unique=True)
    reference_id = models.CharField(('Reference ID'), max_length=125, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    recipient_name = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='transactions')
    description = models.TextField()
    space_paidfor = models.ForeignKey(HouseModel, on_delete=models.PROTECT, null=True, blank=True)
    completed = models.BooleanField(default=False)
    # transaction_date = models.DateField(default=timezone.now().date)
    date_created = models.DateTimeField(auto_now_add=True)
    
    


class CardDetail(models.Model):
    # hash the cvv before saving to the database
    profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name="card_detail")
    card_no = models.CharField(max_length=50)
    cvv = models.CharField(max_length=5)
    expirydate = models.CharField(max_length=10)
    

class Invoice(models.Model):
    profile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="invoice")
    year = models.DateField(default=timezone.now)
    house_for = models.ForeignKey(HouseModel, on_delete=models.SET_NULL, null=True,  related_name="invoice")
    
    description = models.CharField(max_length=200, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Closed")],
        default="active",
    )

    class Meta:
        ordering = ["profile", "house_for"]

    def __str__(self):
        return f"{self.profile}"

    def balance(self):
        payable = self.total_amount_payable()
        paid = self.total_amount_paid()
        return payable - paid

    def amount_payable(self):
        items = InvoiceItem.objects.filter(invoice=self)
        total = 0
        for item in items:
            total += item.amount
        return total

    def total_amount_payable(self):
        return self.balance_from_previous_term + self.amount_payable()

    def total_amount_paid(self):
        receipts = Receipt.objects.filter(invoice=self)
        amount = 0
        for receipt in receipts:
            amount += receipt.amount_paid
        return amount

    def get_absolute_url(self):
        return reverse("invoice-detail", kwargs={"pk": self.pk})

    @property
    def get_profile(self):
        return User.objects.filter(username=self.request.user)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoice_item")
    description = models.CharField(max_length=200)
    amount = models.IntegerField()

class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    date_paid = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Receipt on {self.date_paid}"