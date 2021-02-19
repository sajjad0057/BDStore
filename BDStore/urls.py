from django.contrib import admin
from django.urls import path,include

# TO show media files : 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Shop.urls')),
    path('account/',include('Login.urls')),
    path('shop/',include('Order.urls')),
    path('payment/',include('Payment.urls')),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
