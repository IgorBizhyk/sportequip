from django.contrib import admin

from products.models import Product, Country


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'country_producer', 'weight', 'price',
    )
    list_filter = ('name', 'country_producer', 'weight', 'price',)


@admin.register(Country)
class AdminCountry(admin.ModelAdmin):
    list_display = (
        'id', 'name',
    )
    list_filter = ('name',)
