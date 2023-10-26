from django import forms
from .models import Employee, Cliente, Gerente, Empleado, Address

class EmployeeAddressForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'  

    # Agrega todos los campos de Address al formulario
    def __init__(self, *args, **kwargs):
        super(EmployeeAddressForm, self).__init__(*args, **kwargs)
        for field_name, field in Address._meta.fields_map.items():
            if field_name != 'id':  # Excluye el campo 'id' de Address si lo tiene
                self.fields[field_name] = field.formfield()

class AddressEmployeeForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__' 


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
