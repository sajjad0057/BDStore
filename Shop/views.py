from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,Category

# Create your views here.


class Home(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name='Shop/home.html'
