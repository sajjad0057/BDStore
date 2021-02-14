from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'ModelNames'
        

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    main_image = models.ImageField(upload_to='media/Products')
    name = models.CharField(max_length=86)
    preview_text = models.TextField(max_length=128,verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1024,verbose_name="Description")
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    
    
    
    

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created']
       

    
    