from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    #link the profile to the user
    user= models.OneToOneField(User);
    
    address = models.CharField(max_length=50);
    phone = models.CharField(max_length=20);
    verifiedEmail = models.BooleanField(default=False)
    verifyEmailCode = models.CharField(max_length=14, unique=False)
    displayHelp = models.BooleanField(default=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Create a profile on the creation of the user connected with this user
post_save.connect(create_user_profile, sender=User)