import io

import requests
from PIL import Image


class ImageOverlay:
    def __init__(self, image_url: str):
        self.image_url = image_url
        self.image: Image.Image = None

    def _get_image(self) -> Image.Image:
        if self.image is None:
            remote_photo_request = requests.get(self.image_url)
            self.image = Image.open(io.BytesIO(remote_photo_request.content), mode='r') \
                .convert('RGBA')
            res = self.image
        else:
            res = self.image.copy()
        return res

    def overlay(self, layers: list[list[Image.Image, tuple[int, int]]]) -> Image.Image:
        bg = self._get_image()
        for image, point in layers:
            bg.paste(image, tuple(dict(point).values()))
        return bg
