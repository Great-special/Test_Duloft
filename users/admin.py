from django.contrib import admin

# Register your models here.
from .models import User, LandLordProfile, LandLordPaymentDetails

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'sur_name', 'username', 
        'email', 'phone_no', 'date_created',
        'is_staff', 'is_landlord'
        ]
    
    list_per_page = 10
    
    # list_editable = [
    #     'sur_name', 'username', 
    #     'email', 'phone_no'   
    #     ]



class LandLordAdmin(admin.ModelAdmin):
    list_display = [
        'user_profile',
        'national_id_number',
        ]
    list_per_page = 10
    
admin.site.register(LandLordProfile, LandLordAdmin)
admin.site.register(LandLordPaymentDetails)