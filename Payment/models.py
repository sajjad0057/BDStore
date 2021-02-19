from django.db import models
from django.conf import settings


# Create your models here.

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.CharField(max_length=264, blank=True)
    zipcode = models.CharField(max_length=8, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=20, blank=True)
    phone_no = models.CharField(max_length=20,blank=True)
    
    
    def __str__(self):
        return f'{self.user.profile.username}\'s billing address'
    
    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]
        for field in fields_name:
            value = getattr(self,field)
            if value is None or value == "":
                return False
        return True
    
    class Meta:
        verbose_name_plural = 'Billing Addresses'