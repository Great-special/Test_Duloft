"""
    working with signals
    You will need the sender Model and the receiver Model
    the signal can either be post_save, per_save
    after which you add it to the apps.py file using
    a function.
    def ready(self):
        import app_name.signals
"""


from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import User, LandLordProfile


@receiver(post_save, sender=LandLordProfile)
def update_user_profile(sender, instance, created, **kwargs):
    userId = instance.user_profile
    print(userId)
    if created:
        user = User.objects.get(username=userId)
        user.is_landlord = True
        user.save()