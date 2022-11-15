import io
import math

import requests
import segno
from PIL import Image
from pydantic import BaseModel


class Size(BaseModel):
    width: int = 100
    height: int = 100

    @property
    def size(self):
        return self.width, self.height


class Qr:
    def __init__(self, msg: str, options: dict, *, format='png', background_image_url=None, error='H'):
        self.msg = msg
        self.options = options
        self.error = error
        self.format = format
        self.background_image_url = background_image_url
        self._img = None
        self._msk = None
        self._scale = None
        self.QRCode = segno.make(msg, error=error)

    @property
    def scale(self) -> int:
        if self._scale is None:
            qr_data = io.BytesIO()
            qrcode = self.QRCode
            qrcode.save(qr_data, kind=self.format, scale=1)
            qr = Image.open(qr_data)
            qr_data.seek(0)
            qr_data.truncate()

            # Now we calculate the scale of the image. We will resize it as well, so we always go one scale up
            qr_scale = math.ceil(self.size.width / qr.size[0])
            self._scale = qr_scale
        return qr_scale

    @property
    def mask(self) -> Image.Image:
        pass

    @property
    def img(self) -> Image.Image:
        if self._img is None:
            qr_data = io.BytesIO()
            if self.background_image_url:
                background_image = requests.get(self.background_image_url)
                background_image_data = io.BytesIO(background_image.content)
                self.qrcode.to_artistic(background=background_image_data,
                                        target=qr_data, kind=self.format, scale=self.scale)
            else:
                self.qrcode.save(qr_data, kind=self.format, scale=self.scale, **self.options)
            qr = Image.open(qr_data)
            if qr.size != (self.size.width, self.size.height):
                qr = qr.resize(self.size.size, Image.Resampling.LANCZOS)

            self._img = qr

        return self._img


class RequestQrCode(BaseModel):
    msg: str
    size: Size = None
    options: dict = None
    background_url: str = None


class ResponseQrCode(BaseModel):
    msg: str
    original_msg: str = None
    size: Size = None
    options: dict = None
    image_url: str = None
