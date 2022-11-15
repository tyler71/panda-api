import io
from urllib.parse import urlparse

from requests import JSONDecodeError
from starlite import State, Partial, post, Request
from starlite.controller import Controller

from ..library import QrGeneration
from ..models import RequestQrCode, ResponseQrCode, Size

from ...core.library import try_shorten_url


class QrCodeController(Controller):
    path = "/qr"

    @post("/")
    async def post_qr_image(self,
                            state: State,
                            request: Request,
                            data: Partial[RequestQrCode],
                            ) -> ResponseQrCode:
        converted_to_url = try_shorten_url(data.msg, state=state, request=request)
        output_url = converted_to_url if converted_to_url is not None else data.msg
        qr = QrGeneration(output_url, data.size, options=data.options, background_image_url=data.background_url)
        qr_img = qr.generate()
        qr_in_memory = io.BytesIO()
        qr_img.save(qr_in_memory, format='png')
        qr_in_memory.seek(0)
        qr_image_url = state.linx.upload(qr_in_memory, randomize_filename=True, expiration_seconds=60)

        res = ResponseQrCode(
            msg=data.msg,
            options=data.options,
            image_url=qr_image_url.json()['direct_url']
        )
        size = Size()
        size.width, size.height = qr_img.size
        res.size = size

        if converted_to_url is not None:
            res.original_msg = data.msg
            res.msg = converted_to_url

        return res
