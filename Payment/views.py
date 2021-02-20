from django.shortcuts import render,HttpResponseRedirect,redirect
from django.urls import reverse
from Order.models import Order
from .models import BillingAddress
from .forms import BillingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# For SSLcommerz API
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal

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
            
    
    return render(request,"Payment/checkout.html",{'form':form,'order_items':order_items,
                                                   'order_total':order_total,'saved_address':saved_address})
    


# For payment :

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get(user=request.user)
    if not saved_address.is_fully_filled():
        messages.info(request,"Please complete shipping address first !")
        return redirect('Payment:checkout')
    if not request.user.profile.is_fully_fielled():
        messages.info(request,"Please complete your Info first !")
        return redirect('Login:profile')
    
    # For SSLCOMMERZ API :
    
    store_id = 'sajja5f61279af322c'
    API_key ='sajja5f61279af322c@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)

    print('request---->',request)
    status_url = request.build_absolute_uri(reverse('Payment:payment_status')) # Returns the absolute URI form of location. If no location is provided, the location will be set to request.get_full_path().
    
    print(status_url)
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                        cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user,ordered=False)[0] # if use get instead of filter ,don't need to be indexing
    orderItems = order_qs.orders_item.all()
    orderItemsCount = order_qs.orders_item.count()
    orderTotals = order_qs.get_total_items()
    mypayment.set_product_integration(total_amount=Decimal(orderTotals),
                                      currency='BDT', product_category='Mixed',
                                      product_name=orderItems, num_of_item=orderItemsCount,
                                      shipping_method='Courier', product_profile='None')

    
    current_user = request.user
    
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email,
                                address1=current_user.profile.address_1,
                                address2=current_user.profile.address_1, city=current_user.profile.city,
                                postcode=current_user.profile.zipcode, country=current_user.profile.country,
                                phone=current_user.profile.phone)
    #print("saved_address.user.profile.full_name ---->>>>>",saved_address.user.profile.full_name)
    mypayment.set_shipping_info(shipping_to=saved_address.user.profile.full_name,
                                address=saved_address.address,
                                city=saved_address.city,
                                postcode=saved_address.zipcode,
                                country=saved_address.country)

    # If you want to post some additional values
    mypayment.set_additional_values(value_a='cusotmer@email.com', value_b='portalcustomerid', value_c='1234', value_d='uuid')

    response_data = mypayment.init_payment()
    print("response_data ***+++***>>",response_data)
    
    return redirect(response_data['GatewayPageURL'])



@login_required
def complete(request):
    return render(request,"Payment/complete.html",)
        
    



























