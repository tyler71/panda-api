import io
import math
import segno
from PIL import Image


class QrGeneration:
    """
    https://segno.readthedocs.io/en/latest/colorful-qrcodes.html
    """

    def __init__(self, *, error_correction: str = 'h'):
        self.error_correction = error_correction

    def generate(self, msg: str, size: tuple = (100, 100), *, options=None) -> Image.Image:
        if options is None:
            options = dict()

        qr_data = io.BytesIO()
        qrcode = segno.make(msg, error=self.error_correction)
        qrcode.save(qr_data, kind='PNG', scale=1, **options)
        qr = Image.open(qr_data)
        if qr.size[0] < size[0]:
            qr_data.seek(0)
            qr_data.truncate()

            qr_scale = math.ceil(size[0] / qr.size[0])
            qrcode.save(qr_data, kind='PNG', scale=qr_scale, **options)
            qr = Image.open(qr_data)
            if qr.size != size:
                qr = qr.resize(size, Image.Resampling.LANCZOS)
        return qr
