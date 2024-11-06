from django.db import models
from products.models import Product
from customers.models import Customer

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        PROCESSING = 'Processing', 'Processing'
        COMPLETED = 'Completed', 'Completed'

    id = models.AutoField(primary_key = True)
    products = models.ManyToManyField(Product, related_name='orders')
    total_amount = models.IntegerField()
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    def calculate_total_amount(self):
        return sum(product.price for product in self.products.all())

    def __str__(self):
        return f'Order {self.id} - {self.customer.name}'
