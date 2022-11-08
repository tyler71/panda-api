import io
from urllib.parse import urlparse

from PIL import Image
from UliEngineering.Math.Coordinates import BoundingBox
from starlite import State, Partial, post
from starlite.controller import Controller

from ..library import QrGeneration, ImageOverlay
from ..models import RequestImageOverlay, ResponseImageOverlay, QrLocation, Size
import numpy as np


# from ...core.library import Yourls


class ImageOverlayController(Controller):
    path = "/image_overlay"
    qr = QrGeneration()

    def _image_box(self, coordinates: QrLocation) -> BoundingBox:
        c = coordinates
        ulx, uly, brx, bry = int(c.upper_left.x), int(c.upper_left.y), int(c.bottom_right.x), int(c.bottom_right.y)
        np_array = np.asarray(((ulx, uly), (brx, bry)))
        box = BoundingBox(np_array)
        return box

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

        img_overlay = ImageOverlay(image_url=data.base_image)

        qr_box = self._image_box(data.qr.location)

        converted_to_url = self._is_url(data.qr.msg, state=state)
        output_url = converted_to_url if converted_to_url is not None else data.qr.msg
        qr_img_size = Size()
        qr_img_size.x, qr_img_size.y = qr_box.width, qr_box.height
        qr_img = self.qr.generate(output_url, size=qr_img_size, background_image_url=data.qr.background_url, options=data.qr.options)

        layered_img = img_overlay.overlay([[qr_img, data.qr.location.upper_left]])
        layered_img_bytes = io.BytesIO()
        layered_img.save(layered_img_bytes, format="PNG")
        layered_img_bytes.seek(0)
        layered_image_url = state.linx.upload(layered_img_bytes, randomize_filename=True)

        res = ResponseImageOverlay(
            image_url=layered_image_url.json()['direct_url']
        )
        return res
