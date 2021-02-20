from django.urls import path
from . import views

app_name = "Payment"

urlpatterns = [
    path('checkout/',views.checkout,name="checkout"),
    path('process/',views.payment,name="payment"),
    path('status/',views.complete,name='payment_status'),
    path('purchase/<val_id>/<tran_id>/',views.purchase,name='purchase'),
    path('orders/',views.user_orders,name='orders'),

]
