from django.contrib import admin

from basket.models import Basket, BasketItem


@admin.register(Basket)
class AdminBasket(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'is_active', 'order_date',
    )
    list_filter = ('user', 'is_active', 'order_date',)


@admin.register(BasketItem)
class AdminBasketItem(admin.ModelAdmin):
    list_display = (
        'id', 'basket', 'product', 'quantity',
    )
    list_filter = ('basket', 'product', 'quantity',)
