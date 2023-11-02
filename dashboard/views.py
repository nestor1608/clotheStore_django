from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView


class DashboardEmployeeView(TemplateView):
    template_name = "dashboard/dashboard_index.html"





class CustomLoginView(LoginView):
    template_name = "account/account_login.html"
    
    
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse('superuser_dashboard')
        elif hasattr(user, 'employee'):
            return reverse('employe_dashboard')
        elif hasattr(user, 'manager'):
            return reverse('manager_dashboard')
        elif hasattr(user, 'customer'):
            return reverse('customer_dashboard')
        return super().get_success_url()




class SuperUserDashboard(TemplateView):
    template_name = "dashboard/dashboard_index.html"
    
    
class EmployeeDashboard(TemplateView):
    template_name = "dashboard/dashboard_index.html"
    
    
class ManagerDashboard(TemplateView):
    template_name = "dashboard/dashboard_index.html"
    
    
    
class CustomerView(TemplateView):
    template_name = "home/index.html"
