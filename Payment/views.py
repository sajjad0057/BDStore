from django.shortcuts import render,HttpResponseRedirect,redirect
from django.urls import reverse
from Order.models import Order,Cart
from .models import BillingAddress
from .forms import BillingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# For SSLcommerz API
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt # for disable csrf verification in SSL API post request
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



@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        #print(payment_data)
        status = payment_data['status']

        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request,' your payment has been completed successfully !')
            return HttpResponseRedirect(reverse('Payment:purchase',kwargs={
                'val_id':val_id,'tran_id':tran_id
            }))
        elif status == 'FAILED':
            messages.warning(request,' Oops ! Your payment had been failed ! Please try again. this page is redirect autometically, please wait 5 sec.')
        
    return render(request,'Payment/complete.html',context={})


def purchase(request,val_id,tran_id):
    '''Here if we use get() query_set,we don't have need to use indexing for access object value,
    otherwise we need  indexing  to access objects value  '''
    order_q = Order.objects.filter(user=request.user,ordered=False)
    #print('order_q---->',order_q)
    #print('order_q[0]---->',order_q[0])
    order_qs = Order.objects.get(user=request.user,ordered=False)
    #print('order_qs---->',order_qs)
    order_qs.ordered=True
    order_qs.paymentId=val_id
    order_qs.orderId=tran_id
    order_qs.save()
    cart_item = Cart.objects.filter(user=request.user,purchased=False)
    #print('cart_item----->',cart_item)
    for item in cart_item:
        #print('item---->',item)
        item.purchased=True
        item.save()
    return HttpResponseRedirect(reverse('Shop:home'))



@login_required
def user_orders(request):
    try:
        orders = Order.objects.filter(user=request.user,ordered=True)
        print(orders)
        dict = {'orders':orders}
        if orders.exists():
            return render(request,'Payment/order.html',context=dict)
        else:
            messages.warning(request,"Yon don't have any active order now ! ")
            return redirect('Shop:home')
            
    except:
        messages.warning(request,"Error Some Thing ! ")
        return redirect('Shop:home')
        
    
        
    



























