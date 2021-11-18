from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard.html'
