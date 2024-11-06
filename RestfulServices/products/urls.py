from django.urls import path
from .views import productListCreateView, productRetrieveUpdateDestroyViews

urlpatterns = [
    path('venues/<int:venue_id>/products/', productListCreateView.as_view(), name='product-list-create'),
    path('venues/<int:venue_id>/products/<int:pk>', productRetrieveUpdateDestroyViews.as_view(), name='product-detail'),
]
