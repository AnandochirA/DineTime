from rest_framework import generics
from .models import Customer
from .serializers import customerSerializer

class customerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = customerSerializer
    

class customerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = customerSerializer
