import io

import requests
from PIL import Image

from ..models import Layer


class ImageOverlay:
    def __init__(self, image_url: str):
        self.image_url = image_url
        self.image: Image.Image = None

    def _get_image(self) -> Image.Image:
        if self.image is None:
            remote_photo_request = requests.get(self.image_url)
            self.image = Image.open(io.BytesIO(remote_photo_request.content), mode='r').convert('RGBA')
            res = self.image
        else:
            res = self.image
        return res

    def overlay(self, layers: list[Layer]) -> Image.Image:
        layered_image = io.BytesIO()
        bg = self._get_image().copy()
        for layer in layers:
            upper_left = tuple[int, int](layer.upper_left.__dict__.values())
            bg.paste(layer.img, upper_left, mask=layer.mask)

        bg.save(layered_image, format='PNG')
        return Image.open(layered_image)
