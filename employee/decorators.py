from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse

# Función de prueba para verificar si el usuario es un cliente
def is_cliente(user):
    return user.groups.filter(name='Cliente').exists()

# Función de prueba para verificar si el usuario es un empleado
def is_empleado(user):
    return user.groups.filter(name='Empleado').exists()

# Decorador para restringir el acceso a la vista del gerente
def gerente_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='Gerente').exists():
            return view_func(request, *args, **kwargs)
        else:
            # Puedes personalizar la respuesta si no es un gerente
            return HttpResponse("No tienes permiso para acceder a esta página.")
    return _wrapped_view

# Decorador para la vista del cliente
def cliente_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_cliente(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("No tienes permiso para acceder a esta página.")
    return _wrapped_view

# Decorador para la vista del empleado
def empleado_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_empleado(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("No tienes permiso para acceder a esta página.")
    return _wrapped_view
