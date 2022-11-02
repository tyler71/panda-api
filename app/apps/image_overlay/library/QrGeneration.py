import io
import math
import segno
from PIL import Image

from app.library import Yourls


class QrGeneration:
    """
    https://segno.readthedocs.io/en/latest/colorful-qrcodes.html
    """

    def __init__(self, *, yourls_domain: str, yourls_signature: str, error_correction: str = 'h'):
        self.error_correction = error_correction
        self.yourls = Yourls(domain=yourls_domain, signature=yourls_signature, method='POST', output='json')

    def generate(self, msg: str, size: tuple = (100, 100), *, qr_options: dict) -> Image.Image:
        shorturl = self.yourls.shorten(msg)
        if shorturl.status_code in (200, 400):
            qr_data = io.BytesIO()
            qrcode = segno.make(shorturl.json()['shorturl'], error=self.error_correction)
            qrcode.save(qr_data, scale=1, **qr_options)
            qr = Image.open(qr_data)
            if qr.size[0] < size[0]:
                qr_scale = math.ceil(size[0] / qr.size[0])
                qrcode.save(qr_data, scale=qr_scale, **qr_options)
                qr = Image.open(qr_data)
                if qr.size != size:
                    qr = qr.resize(size, Image.Resampling.LANCZOS)
        else:
            qr = None
        return qr
