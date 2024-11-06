from django.urls import path
from .views import (orderListCreateView, orderRetrieveUpdateDestroyView)

urlpatterns = [
    path('orders/', orderListCreateView.as_view(), name = 'order-list-create'),
    path('orders/<int:pk>/', orderRetrieveUpdateDestroyView.as_view(), name = 'order-detail'),
]