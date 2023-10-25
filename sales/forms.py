from django import forms
from .models import Venta, ItemVenta

class ItemVentaForm(forms.ModelForm):
    class Meta:
        model = ItemVenta
        fields = ['producto', 'cantidad']

ItemVentaFormSet = forms.inlineformset_factory(Venta, ItemVenta, form=ItemVentaForm, extra=1)

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemventa_formset = ItemVentaFormSet(*args, **kwargs)

