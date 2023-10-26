from django.urls import path
from . import views

urlpatterns = [
    path('cliente/nuevo/', views.ClienteCreateView.as_view(), name='crear_cliente'),
    path('empleado/nuevo/', views.EmpleadoCreateView.as_view(), name='crear_empleado'),
    path('empleados/', views.EmpleadoListView.as_view(), name='empleado_list'),
    path('empleado/editar/<int:pk>/', views.EmpleadoUpdateView.as_view(), name='editar_empleado'),
    path('empleado/eliminar/<int:pk>/', views.EmpleadoDeleteView.as_view(), name='eliminar_empleado'),
    # Otras URL según tus necesidades
]
