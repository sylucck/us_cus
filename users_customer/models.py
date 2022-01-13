from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True, help_text="Insert your name")
    image = models.ImageField(default='default.png', upload_to='')

    def __str__(self):
        """String for representing a model object"""
        return self.name



class Customer(models.Model):
    name = models.OneToOneField(Profile,  on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        """String for representing a model object"""
        return (self.name)


