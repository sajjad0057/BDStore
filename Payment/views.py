from django.shortcuts import render,HttpResponseRedirect
from Order.models import Order
from .models import BillingAddress
from .forms import BillingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0] # get_or_create querySet return a tuple.
    form = BillingForm(instance=saved_address)
    if request.method == "POST":
        form = BillingForm(request.POST,instance=saved_address)
        if form.is_valid():       
            form.save()
            form = BillingForm(instance=saved_address)
            messages.info(request,"Shipping address saved !")
    order_qs = Order.objects.filter(user = request.user)[0]
    order_items = order_qs.orders_item.all()
    order_total = order_qs.get_total_items()
            
    
    return render(request,"Payment/checkout.html",{'form':form,'order_items':order_items,'order_total':order_total,'saved_address':saved_address})
