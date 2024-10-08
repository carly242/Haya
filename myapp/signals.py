from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from allauth.account.signals import user_logged_in
import logging


logger = logging.getLogger(__name__)



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating profile for user: {instance}")
        Profile.objects.create(user=instance)
