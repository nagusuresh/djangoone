from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        if len(self.name) < 3:
            raise ValidationError({'name': "Product name must be at least 3 characters long."})

        if self.discount > self.price:
            raise ValidationError({'discount': "Discount can't exceed the product price."})

        if self.stock == 0:
            self.is_active = False
   

    def final_price(self):
        return self.price - self.discount

    def __str__(self):
        return self.name