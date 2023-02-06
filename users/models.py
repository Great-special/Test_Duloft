from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from payment_manager.bankList import BankList

from .utils import generate_ref_code



class UserManager(BaseUserManager):
    use_in_migrations=True
    
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
    
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,password,username,email=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_landlord',True)


        if extra_fields.get('is_staff') is not True:
            return ValueError('Superuser must be assign is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            return ValueError('Superuser must be assign is_superuser=True')

        if extra_fields.get('is_landlord') is not True:
            return ValueError('Superuser must be assign is_landlord=True')

        return self._create_user(username, email, password, **extra_fields)


    def create_landlord(self,password,username,email=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_landlord',True)

        if extra_fields.get('is_landlord') is not True:
            return ValueError('Author must be assign is_landlord=True')

        return self._create_user(username, email, password, **extra_fields)


    def create_user(self,password,username,email=None,**extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault('is_landlord',False)
        return self._create_user(username, email, password, **extra_fields)

        

class User(AbstractBaseUser,PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    first_name=models.CharField(max_length=150,null=True,blank=True)
    sur_name=models.CharField(max_length=150,null=True,blank=True)
    other_name = models.CharField(max_length=150,null=True,blank=True)
    
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        null=True,blank=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )
    email = models.EmailField(("email address"), blank=True)
    phone_no=models.CharField(max_length=150,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True)

    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_landlord=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects=UserManager()

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s %s" % (self.first_name, self.other_name, self.sur_name)
        return full_name.strip()

    
    def get_reversed_name(self):
        """
        Return the sur_name plus the first_name, with a space in between.
        """
        full_name = "%s %s %s" % (self.sur_name, self.other_name, self.first_name)
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)





class LandLordProfile(models.Model):
    user_profile = models.OneToOneField(User, related_name="landLord", on_delete=models.CASCADE, null=True, blank=True)
    referral_code = models.CharField(max_length=16, unique=True, blank=True, null=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='referrals')
    national_id_number = models.PositiveIntegerField(unique=True)
    national_id_image = models.ImageField(upload_to='doucments/IDs/')
    profile_photo = models.ImageField(upload_to='doucments/profilePhotos/')

    
    def __str__(self) -> str:
        return self.user_profile.username
    
    def save(self, *args, **kwargs):
        if self.referral_code == "":
            referral_code = "DU" + generate_ref_code()
            object_with_similar_ref = LandLordProfile.objects.filter(referral_code=referral_code)
            if object_with_similar_ref:
                referral_code = "DU" + generate_ref_code()
            else:
                self.referral_code = referral_code
        super().save(*args, **kwargs)
    

class LandLordPaymentDetails(models.Model):
    bank_name = models.CharField(max_length=100, choices=BankList, default='Access Bank', verbose_name="Bank Name")
    account_name = models.CharField(max_length=100)
    account_number = models.PositiveIntegerField()
    user_profile = models.OneToOneField(User, related_name="paymentdetail", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user_profile.username