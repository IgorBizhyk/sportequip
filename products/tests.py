from django.urls import reverse
from mixer.backend.django import mixer

from basket.models import Basket
from products.models import Product
from sportequip.tests import BaseTest


class TestProductListView(BaseTest):
    def setUp(self):
        self.user = self.create_and_login()
        self.product = mixer.blend(Product)

    def test_get_product_list(self):
        resp = self.client.get(reverse('products:product-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context_data['object_list'][0], self.product)


class TestAddToBasketView(BaseTest):
    def setUp(self):
        self.user = self.create_and_login()
        self.product = mixer.blend(Product)

    def test_add_to_basket(self):
        resp = self.client.post(reverse('products:add-to-basket', args=[self.product.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Basket.objects.get(user=self.user, is_active=True).items.first().product, self.product)
