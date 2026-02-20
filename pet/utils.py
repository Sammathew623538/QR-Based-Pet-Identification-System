
import qrcode
from django.utils.text import slugify
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

def generate_unique_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.pet_name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(unique_slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=instance.id or 'new' # Fallback if ID is not yet available, usually handled by post_save or UUID
        )
        return generate_unique_slug(instance, new_slug=new_slug)
    return slug

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    file_buffer = File(buffer, name=f'qr_code.png')
    return file_buffer
