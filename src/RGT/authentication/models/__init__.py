from django.db import models


class PassRecoverCode(models.Model):
    email = models.EmailField()
    linkCode = models.CharField(max_length=14, unique=False)
    dateTime = models.DateTimeField(auto_now_add=True)
    linkUsed = models.BooleanField(default=False)
    linkExpired = models.BooleanField(default=False)

    class Meta:
        app_label = 'authentication'
