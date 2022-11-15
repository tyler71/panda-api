import io

from starlite import State, Partial, post, Request
from starlite.controller import Controller

from ..library import QrGeneration, ImageOverlay
from ..models import RequestImageOverlay, ResponseImageOverlay, QrLocation, Size, Point, Layer
from ...core.library import try_shorten_url


# from ...core.library import Yourls


class ImageOverlayController(Controller):
    path = "/"

    @post("/")
    async def post_image_overlay(self,
                                 state: State,
                                 request: Request,
                                 data: Partial[RequestImageOverlay],
                                 ) -> ResponseImageOverlay:
        img_overlay = ImageOverlay(image_url=data.base_image)

        qr_box = data.qr.location.box

        # Try to shorten the msg if it is an url
        converted_to_url = try_shorten_url(data.qr.msg, state=state, request=request)
        output_url = converted_to_url if converted_to_url is not None else data.qr.msg

        # Identify the size of the qr code. We're looking to ensure it is scaled high enough
        # to the desired size.
        qr_img_size = Size()
        qr_img_size.width, qr_img_size.height = qr_box.width, qr_box.height
        qr = QrGeneration(output_url, size=qr_img_size,
                          background_image_url=data.qr.background_url, **data.qr.options)
        qr_img = qr.generate()

        # overlay accepts multiple layers and a mask, but here we are just putting in one layer.
        # This may change. The layer we're putting on is the qr code
        layer = Layer()
        layer.__dict__ = {
            "img": qr_img,
            "upper_left": data.qr.location.upper_left
        }

        layered_img = img_overlay.overlay([layer])

        # With the image flattened, we're going to save it to memory and upload the file
        layered_img_bytes = io.BytesIO()
        layered_img.save(layered_img_bytes, format="PNG")
        layered_img_bytes.seek(0)
        layered_image_url = state.linx.upload(layered_img_bytes, randomize_filename=True)

        res = ResponseImageOverlay(
            image_url=layered_image_url.json()['direct_url']
        )
        return res
