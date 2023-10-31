from django import forms
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.contrib.auth import get_user
from PIL import Image
from .models import ProductDataGeneral, Category,ValuesPriceProduct,SubCategory



class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductDataGeneral
        fields = ['name', 
                'category', 
                'brand', 
                'provider', 
                'number_serie', 
                'description', 
                'imagen_url']

    def save(self, commit=True, request=None):
        # Obtiene la imagen del formulario
        image = self.cleaned_data['imagen_url']

        # Redimensiona la imagen (ajusta según tus necesidades)
        max_size = (800, 800)  # Tamaño máximo de la imagen
        img = Image.open(image)
        img.thumbnail(max_size)

        # Guarda la imagen en un búfer
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='WEBP')  # Puedes cambiar el formato según lo necesites
        img_buffer.seek(0)

        # Sube la imagen a Google Drive
        image_name = f"product_{self.instance.name}_{self.instance.product_id}.jpg"  # Cambia el nombre de la imagen según tus necesidades
        image_url = self.upload_to_google_drive(image_name, img_buffer)

        # Crea un nuevo producto
        product = super().save(commit=False)
        product.imagen_url = image_url
        
        
        # Get the current user
        user = get_user(request)
        
        # Create a new product with the user assigned
        #product = super().save(commit=False)
        product.user_create_price = user  # Assign the current user

        if commit:
            product.save()

        return product

    def upload_to_google_drive(self, image_name, image_buffer):
        drive_service = build('drive', 'v3', credentials='961887015961-a5q61h0hrg4p2s6jvrdet5qnhgc6vmfn.apps.googleusercontent.com')

        # Sube la imagen a Google Drive
        media = MediaFileUpload(
            io.BytesIO(image_buffer.read()),
            mimetype='image/jpeg',  # Cambia el tipo MIME según el formato de la imagen
        )
        file_metadata = {'name': image_name}
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
        ).execute()

        # Obtiene la URL de la imagen en Google Drive
        image_url = f"https://drive.google.com/file/d/{file['id']}/view"

        return image_url

class ValuePriceForm(forms.ModelForm):
    
    class Meta:
        model = ValuesPriceProduct
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__'
