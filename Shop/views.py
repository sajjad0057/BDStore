from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product,Category


# Create your views here.


class Home(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name='Shop/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(category=Category.objects.all())
        return context


class productDetail(LoginRequiredMixin,DetailView):
    model = Product
    template_name = 'Shop/product_details.html'