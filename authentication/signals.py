# authentication/signals.py

from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        # Import the model class here to avoid AppRegistryNotReady error
        from .models import UserProfile
        # Connect the signal handler to the post_save signal of the User model
        post_save.connect(create_user_profile, sender=User)
