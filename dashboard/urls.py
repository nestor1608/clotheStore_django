from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from employee.decorators import login_required, empleado_required
# from .views import JefeView,EmpleadoView, DeveloperView



urlpatterns = [
    path('dashboard/', empleado_required(views.DashboardEmployeeView.as_view()), name='dashboard_index'),
    path('dashboard/login/', views.CustomLoginView.as_view(), name='custom_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('superuser_dashboard/', views.SuperUserDashboard.as_view(), name='superuser_dashboard'),
    path('superuser_dashboard/', views.EmployeeDashboard.as_view(), name='superuser_dashboard'),
    path('superuser_dashboard/', views.ManagerDashboard.as_view(), name='superuser_dashboard'),
    path('superuser_dashboard/', views.CustomerView.as_view(), name='superuser_dashboard'),
]
