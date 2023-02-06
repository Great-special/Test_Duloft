from django.contrib import admin

# Register your models here.


from .models import Payment, TransactionDetail, Invoice, InvoiceItem

admin.site.register([Payment, TransactionDetail, Invoice, InvoiceItem])

