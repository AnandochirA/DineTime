from rest_framework import generics
from .models import venue
from .serializers import venueSerializer

class venueListCreateView(generics.ListCreateAPIView):
    queryset = venue.objects.all()
    serializer_class = venueSerializer

class venueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = venue.objects.all()
    serializer_class = venueSerializer
    
