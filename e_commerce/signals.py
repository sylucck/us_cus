from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *

#we want a user profile to be created for each new user


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

#saving it
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.customer.save()