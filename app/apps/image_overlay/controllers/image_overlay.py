import io
from urllib.parse import urlparse

from PIL.Image import Image
from UliEngineering.Math.Coordinates import BoundingBox
from starlite import State, Partial, post
from starlite.controller import Controller

from ..library import QrGeneration, ImageOverlay
from ..models import RequestImageOverlay, ResponseImageOverlay
import numpy as np


# from ...core.library import Yourls


class ImageOverlayController(Controller):
    path = "/image_overlay"
    qr = QrGeneration()

    def _image_size(self, coordinates: tuple[(int, int), (int, int)]) -> tuple[int, int]:
        np_array = np.asarray(coordinates)
        BoundingBox(np_array)

    def _is_url(self, msg: str, *, state: State) -> str:
        o = urlparse(msg)
        if o.scheme != '':
            res = state.yourls.shorten(o.geturl()).json()['shorturl']
        else:
            res = None
        return res

    @post("/")
    async def post_image_overlay(self,
                                 state: State,
                                 data: Partial[RequestImageOverlay],
                                 ) -> ResponseImageOverlay:

        img_overlay = ImageOverlay(image_url=data.image_url)

        qr_size = self._image_size(data.qr_location)
        qr_image = self.qr.generate(data.qr_msg)

        converted_to_url = self._is_url(data.msg, state=state)
        output_url = converted_to_url if converted_to_url is not None else data.msg
        qr_img = self.qr.generate(output_url, data.size, options=data.options)
        qr_in_memory = io.BytesIO()
        qr_img.save(qr_in_memory, format='png')
        qr_in_memory.seek(0)

        layered_img = img_overlay.overlay([Image.open(qr_in_memory), (200, 300)])
        layered_image_url = state.linx.upload(layered_img)

        res = ResponseImageOverlay(
            image_url=layered_image_url.json()['direct_url']
        )
        return res
