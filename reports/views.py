from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View

from reports.utils import SalesReport


class BaseCSVReportView(LoginRequiredMixin, View):
    """Base class for the downloading reports"""
    http_method_names = ('get',)
    report_class = None
    report_name = None

    def get(self, *args, **kwargs):
        now = datetime.now().strftime("%m-%d-%Y")
        buffer_report = self.report_class().result()
        response = HttpResponse(buffer_report, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={self.report_name}_report_{now}.csv'
        return response


class SalesReportView(BaseCSVReportView):
    report_class = SalesReport
    report_name = 'sales_report'
