import io
import math
import segno
from PIL import Image
from urllib.request import urlopen

from ..models import Size

class QrGeneration:
    """
    https://segno.readthedocs.io/en/latest/colorful-qrcodes.html
    """

    def __init__(self, *, error_correction: str = 'h'):
        self.error_correction = error_correction

    def generate(self, msg: str, size: Size, *, background_image_url: str = None, options=None) -> Image.Image:
        if options is None:
            options = dict()

        # Here we are making the initial qr code image. We want the size of it
        # so we can calculate the correct size later
        qr_data = io.BytesIO()
        qrcode = segno.make(msg, error=self.error_correction)
        qrcode.save(qr_data, kind='png', scale=1)
        qr = Image.open(qr_data)
        qr_data.seek(0)
        qr_data.truncate()

        # Now we calculate the scale of the image. We will resize it as well, so we always go one scale up
        qr_scale = math.ceil(size.x / qr.size[0])
        if background_image_url:
            with urlopen(background_image_url) as bg_url_data:
                qrcode.to_artistic(background=bg_url_data, target=qr_data, kind='png', scale=qr_scale)
        else:
            qrcode.save(qr_data, kind='PNG', scale=qr_scale, **options)
        qr = Image.open(qr_data)
        if qr.size != (size.x, size.y):
            qr = qr.resize((size.x, size.y), Image.Resampling.LANCZOS)

        return qr
