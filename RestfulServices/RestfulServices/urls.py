from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/customer/', include('customers.urls')),
    path('api/order/', include('orders.urls')),
    path('api/product/', include('products.urls')),
    path('api/venue/', include('venues.urls')),
]
