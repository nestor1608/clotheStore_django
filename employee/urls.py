from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('created_employee/', views.CreateEmployeeAddressView.as_view(), name='employee_create'),
    path('list_employee/', views.EmployeeListView.as_view(), name='employee_list'),
    
    path('<int:empleado_id>/marcar-entrada/', views.MarkEntryView.as_view(), name='mark_entry'),
    path('<int:empleado_id>/marcar-salida/', views.MarkExitView.as_view(), name='mark_exit'),
]

