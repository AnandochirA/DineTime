from django.db import models

class venue(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    slogan = models.TextField(max_length = 100)
    address = models.CharField(max_length = 255)

    def __str__(self):
        return self.name
