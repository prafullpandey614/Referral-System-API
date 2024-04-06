from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=4)
    referral_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
class Referral(models.Model):
    referrer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="referrer")
    referred = models.ForeignKey(User,on_delete=models.CASCADE,related_name="referred")
    refferal_code = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now_add=True)
    