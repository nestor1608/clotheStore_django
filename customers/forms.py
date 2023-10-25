from django import forms
from .models import Customer, AddressCustomer

class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'  # Incluye todos los campos de Customer

    # Agrega todos los campos de Address al formulario
    def __init__(self, *args, **kwargs):
        super(CustomerAddressForm, self).__init__(*args, **kwargs)
        for field_name, field in AddressCustomer._meta.fields_map.items():
            if field_name != 'id':  # Excluye el campo 'id' de Address si lo tiene
                self.fields[field_name] = field.formfield()

class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressCustomer
        fields = '__all__'  # Incluye todos los campos de Customer



