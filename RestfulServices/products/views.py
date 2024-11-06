from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .serializers import productSerializer

class productListCreateView(generics.ListCreateAPIView):
    serializer_class = productSerializer

    def get_queryset(self):
        venue_id = self.kwargs['venue_id']
        return Product.objects.filter(venue_id=venue_id)
class productRetrieveUpdateDestroyViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = productSerializer