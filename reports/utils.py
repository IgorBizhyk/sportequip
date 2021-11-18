import csv
import io
from abc import ABC, abstractmethod
from typing import List

from django.db.models import QuerySet, Q

from basket.models import Basket


class BaseReport(ABC):
    """Base class for report, inherit it and override methods you need.
    You must override abstract methods.
    """

    @abstractmethod
    def get_querysets(self) -> List[QuerySet]:
        """Get report querysets. Override and return querysets you need to work with"""
        pass

    @abstractmethod
    def get_headers(self) -> List[str]:
        """Get report headers. Override this method and return list of headers"""
        pass

    @abstractmethod
    def prepare_data(self, *queryset: QuerySet) -> list:
        """Prepare data in proper format
        :param queryset: queryset
        :return report data
        """
        pass

    def create_report(self, headers: List[str], data: list):
        """Create report from headers and data.
        :param headers: list of headers
        :param data: list of rows
        :return buffer with report data"""
        buffer = io.StringIO()
        wr = csv.writer(buffer)
        # set headers
        wr.writerow(headers)
        if data:
            # insert rows
            wr.writerows(data)
        buffer.seek(0)
        return buffer

    def result(self):
        """Prepare the report result in buffer and return it"""
        querysets = self.get_querysets()
        data = self.prepare_data(*querysets)
        return self.create_report(self.get_headers(), data)


class SalesReport(BaseReport):

    def get_querysets(self):
        orders = Basket.objects.filter(is_active=False).order_by('order_date')
        return [orders]

    def get_headers(self):
        return ['Order id', 'Customer', 'Product', 'Quantity', 'Price', 'Total price', 'Order date']

    def prepare_data(self, orders):
        product_data = []
        if orders:
            for order in orders:
                for item in order.items.all():
                    product_data.append(
                        [
                            order.id,
                            order.user.email,
                            item.quantity,
                            item.product.price,
                            order.total_price,
                            order.order_date.strftime("%d-%m-%Y")
                        ]
                    )
                product_data.append(['' * len(self.get_headers())])

        return product_data
