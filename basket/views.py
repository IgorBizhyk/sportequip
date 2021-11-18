from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic.list import BaseListView, MultipleObjectTemplateResponseMixin

from basket.models import Basket, BasketItem


class RemoveBasketItemView(LoginRequiredMixin, View):
    def post(self, request, basket_item_id):
        basket, _ = Basket.objects.get_or_create(user=request.user, is_active=True)
        basket_item = get_object_or_404(BasketItem, id=basket_item_id, basket=basket)
        basket_item.delete()
        messages.info(request, "The product was removed from basket.")
        return redirect("basket:basket-list")


class BasketListView(LoginRequiredMixin, MultipleObjectTemplateResponseMixin, BaseListView):
    model = BasketItem
    template_name = 'basket/basket_list.html'
    success_url = reverse_lazy('basket:basket-items-list')

    def get_queryset(self):
        basket, _ = Basket.objects.get_or_create(user=self.request.user, is_active=True)
        return self.model.objects.filter(basket=basket.pk)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BasketListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['basket'] = Basket.objects.get(user=self.request.user, is_active=True)
        return context


class OrderView(LoginRequiredMixin, View):
    def post(self, request):
        basket, _ = Basket.objects.get_or_create(user=request.user, is_active=True)
        if not basket.items.all():
            messages.info(request, "Your basket is empty.")
            return redirect("basket:basket-list")
        basket.is_active = False
        basket.order_date = timezone.now()
        basket.save()

        Basket.objects.create(user=request.user, is_active=True)
        messages.success(request, f"Yor have made an order. Total price: {basket.total_price} USD")
        return redirect("basket:basket-list")
