from django.urls import path
from .views import (venueListCreateView, venueRetrieveUpdateDestroyView)

urlpatterns = [
    path('venues/', venueListCreateView.as_view(), name='venue-list-create'),
    path('venues/<int:pk>/', venueRetrieveUpdateDestroyView.as_view(), name='venue-detail'),
]
