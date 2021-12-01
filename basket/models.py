from django.db import models

from authentication.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    order_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.id}'

    @property
    def total_price(self):
        return sum([item.item_price for item in self.items.all()])


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_price(self):
        return self.quantity * self.product.price
