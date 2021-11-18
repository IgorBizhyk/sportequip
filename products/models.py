from django.db import models


class Product(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    country_producer = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL)
    weight = models.DecimalField(max_digits=7, decimal_places=3)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
