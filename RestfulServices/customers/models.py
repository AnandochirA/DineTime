# customers/models.py
from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=20)
    balance = models.IntegerField()
    email = models.EmailField()
    phoneNumber = models.TextField()
    def __str__(self):
        return self.name
