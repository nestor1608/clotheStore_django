from django.urls import path
from . import views
from employee.decorators import login_required, empleado_required
# from .views import JefeView,EmpleadoView, DeveloperView

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', empleado_required(views.PruevaIndex.as_view()), name='dashboard_index'),
]
