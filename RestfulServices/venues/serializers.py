from rest_framework import serializers
from .models import venue

class venueSerializer(serializers.ModelSerializer):
    class Meta:
        model = venue
        fields = '__all__'
        