from django import forms
from .models import ProductDataGeneral, Category,ValuesPriceProduct,Article



class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductDataGeneral
        fields = '__all__'



class ValuesPriceProductForm(forms.ModelForm):
    class Meta:
        model = ValuesPriceProduct
        fields = '__all__'  # Agrega los campos necesarios aquí

    def __init__(self, *args, **kwargs):
        id_product = kwargs.pop('id_product', None)
        super(ValuesPriceProductForm, self).__init__(*args, **kwargs)
        if id_product:
            self.fields['id_product'].widget = forms.HiddenInput()
            self.initial['id_product'] = id_product



class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__'
        
class SubCategoryForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = '__all__'



