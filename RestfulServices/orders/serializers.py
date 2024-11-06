from rest_framework import serializers
from .models import Order 
from products.models import Product

class orderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all()
    )
    class Meta:
        model = Order
        fields = '__all__'
    