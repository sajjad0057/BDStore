from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Order.models import Cart,Order
from Shop.models import Product


# Create your views here.

@login_required
def add_to_cart(request,pk):
    item = Product.objects.get(pk=pk)
    order_item = Cart.objects.get_or_create(item = item,user=request.user,purchased=False)
    order_qs = Order.objects.filter(user = request.user,ordered=False)
    print("order_qs------> ",order_qs)
    #print("request.path_info --- >",request.path_info)
    #print("request.path ---- >",request.path)
    print("previous page--->",request.META.get('HTTP_REFERER'))
    if order_qs.exists():
        print("order_qs[0]--->",order_qs[0])
        order = order_qs[0]
        print("order------> ",order)
        if order.orders_item.filter(item=item).exists():
            order_item[0].quantity +=1
            order_item[0].save()
            messages.info(request,'This Item Quantity is Updated!')
            #return redirect('Shop:home')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect to previous page .
        else:
            order.orders_item.add(order_item[0])
            messages.info(request,"This Item is Added To cart")
            #return redirect('Shop:home')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # Redirect to previous page .
    else:
        order = Order(user=request.user)
        order.save()
        order.orders_item.add(order_item[0])
        messages.info(request,"This Item is Added To cart")
        #return redirect('Shop:home')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect to previous page .
         
