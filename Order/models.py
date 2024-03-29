from django.db import models
from django.conf import settings
from Shop.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')
    item = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product')
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.quantity} X {self.item}'
    
    
    def get_total(self):    # User define 
        total = self.item.price * self.quantity
        float_total = format(total,'0.2f')
        return float_total
    
    

class Order(models.Model):
    orders_item = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264,blank=True,null=True)
    orderId = models.CharField(max_length=264,blank=True,null=True)
    
    def __str__(self):
        return f'{self.user} \'s  order'
    
    
    
    def get_total_items(self):  #User define
        #print("self.orders_item.all()--->",self.orders_item.all())
        total = 0
        for order_item in self.orders_item.all():
            #print("order_item.get_total() ---",order_item.get_total())
            total += float(order_item.get_total())
        return total
        
    
        
    