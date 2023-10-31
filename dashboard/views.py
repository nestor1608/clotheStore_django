from django.shortcuts import render
from django.views.generic import TemplateView



class DashboardEmployeeView(TemplateView):
    template_name = "dashboard/dashboard_index.html"
