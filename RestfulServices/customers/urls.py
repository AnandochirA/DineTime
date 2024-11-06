from django.urls import path
from .views import (customerListCreateView , customerRetrieveUpdateDestroyView)

urlpatterns = [
    path('customers/', customerListCreateView.as_view(), name = 'order-list-create'),
    path('customers/<int:pk>/', customerRetrieveUpdateDestroyView.as_view(), name = 'order-detail'),
]