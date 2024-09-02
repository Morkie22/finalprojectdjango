# myapp/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    img = models.ImageField(upload_to='products/', default='products/default.jpg')

    def __str__(self):
        return self.name
