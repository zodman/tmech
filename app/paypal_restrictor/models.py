from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PaypalAccountBase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="paypalaccount")    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True
