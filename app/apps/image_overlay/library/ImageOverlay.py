import io

import requests
from PIL import Image
from . import QrGeneration


class ImageOverlay:
    def __init__(self, image_url: str, qr_position: tuple):
        self.image_url = image_url
        self.qr_position = qr_position
        self.image: Image.Image

    def _get_image(self) -> Image.Image:
        if self.image is None:
            remote_photo_data = io.BytesIO()

            remote_photo_request = requests.get(self.image_url)
            remote_photo = Image.open(io.BytesIO(remote_photo_request.content), mode='r')
            remote_photo.save(remote_photo_data, format="PNG")
            self.image = Image.open(remote_photo_data).convert('RGBA')
            return self.image

