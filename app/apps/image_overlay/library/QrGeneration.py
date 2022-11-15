import io
import math

import requests
import segno
from PIL import Image

from ..models import Size
from starlite import Response, HTTPException


class QrGeneration:
    """
    https://segno.readthedocs.io/en/latest/colorful-qrcodes.html
    """

    def __init__(self, msg, size: Size, background_image_url: str = None, *, error_correction: str = 'h', **options):
        if options is None:
            options = dict()
        self.error_correction = error_correction
        self.msg = msg
        self.size = size
        self.background_image_url = background_image_url
        self.options = options

        if options.get('options', None) is not None and background_image_url is not None:
            raise HTTPException("Cannot use both options and background_url at the same time")

    def gen_mask(self):
        pass

    @property
    def img(self) -> Image.Image:
        return self.generate()

    def generate(self) -> Image.Image:
        # Here we are making the initial qr code image. We want the size of it
        # so we can calculate the correct size later
        qr_data = io.BytesIO()
        qrcode = segno.make(self.msg, error=self.error_correction)
        qrcode.save(qr_data, kind='png', scale=1)
        qr = Image.open(qr_data)
        qr_data.seek(0)
        qr_data.truncate()

        # Now we calculate the scale of the image. We will resize it as well, so we always go one scale up
        qr_scale = math.ceil(self.size.x / qr.size[0])
        if self.background_image_url:
            background_image = requests.get(self.background_image_url)
            background_image_data = io.BytesIO(background_image.content)
            qrcode.to_artistic(background=background_image_data, target=qr_data, kind='png', scale=qr_scale)
        else:
            qrcode.save(qr_data, kind='PNG', scale=qr_scale, **self.options)
        qr = Image.open(qr_data)
        if qr.size != (self.size.x, self.size.y):
            qr = qr.resize((self.size.x, self.size.y), Image.Resampling.LANCZOS)

        return qr
