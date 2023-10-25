from django.conf import settings
import os
import io
import tempfile
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image
from .models import Product

def upload_to_google_drive( image_name, image_buffer):
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

def process_and_upload_image(product, image_path, image_name):
    # Realiza cualquier procesamiento adicional que desees en la imagen aquí

    # Sube la imagen a Google Drive
    image_url = upload_to_google_drive(image_path, image_name)

    # Actualiza el campo de imagen del producto con la URL
    product.imagen = image_url
    product.save()


def process_image(image):
        # Redimensiona la imagen (ajusta según tus necesidades)
        max_size = (800, 800)  # Tamaño máximo de la imagen
        img = Image.open(image)
        img.thumbnail(max_size)
        
        # Guarda la imagen en un búfer
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')  # Puedes cambiar el formato según lo necesites
        img_buffer.seek(0)

        return img_buffer
