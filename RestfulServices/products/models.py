from django.db import models
from venues.models import venue

class Product(models.Model):
    id = models.AutoField(primary_key = True)
    venue_id = models.ForeignKey(venue, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    price = models.IntegerField()
    description = models.TextField()
    minutesToTake = models.IntegerField()
    
    def __str__ (self):
        return self.name