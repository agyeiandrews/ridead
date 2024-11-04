# yourapp/utils.py

import qrcode
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid

def generate_qr_code(data):
    qr = qrcode.make(data)
    qr_image = ContentFile(b'')  # Create a blank file-like object
    qr.save(qr_image, format='PNG')

    # Save the QR code image to a directory (you may want to customize the path)
    file_name = f'qr_codes/{uuid.uuid4()}.png'
    default_storage.save(file_name, qr_image)

    return default_storage.url(file_name)
