import io

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

    def _size(self):
        pass

    def generate(self, msg: str, size: tuple = (100, 100), *, qr_options: dict) -> Image.Image:
        qr_data = io.BytesIO()

        qrcode = segno.make(msg, error=self.error_correction)
        qrcode.save(qr_data, **qr_options)
        # qrcode.save(qr_data, kind='PNG', dark='purple', border=1, scale=1)
        qr = Image.open(qr_data)
        return qr
