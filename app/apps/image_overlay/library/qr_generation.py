import io

import segno
from PIL import Image

import library


def generate_qr(msg: str, size: tuple = (100, 100), *, error_correction: str = 'h', qr_options: dict) -> Image.Image:
        """
        https://segno.readthedocs.io/en/latest/colorful-qrcodes.html
        """
        qr_data = io.BytesIO()

        qrcode = segno.make(msg, error=error_correction)
        qrcode.save(qr_data, **qr_options)
        # qrcode.save(qr_data, kind='PNG', dark='purple', border=1, scale=1)
        qr = Image.open(qr_data)
        qr
