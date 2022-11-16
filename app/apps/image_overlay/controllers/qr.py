import io
from urllib.parse import urlparse

from requests import JSONDecodeError
from starlite import State, Partial, post, Request
from starlite.controller import Controller

from ..library import QrGeneration
from ..models import RequestQrCode, ResponseQrCode, Size, Qr

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

        qr = Qr(msg=output_url, size=data.size, options=data.options, background_image_url=data.background_url)

        img_bytes = io.BytesIO()
        qr.img.save(img_bytes, format=qr.format)
        img_bytes.seek(0)
        qr_image_url = state.linx.upload(img_bytes, randomize_filename=True, expiration_seconds=60)

        res = ResponseQrCode(
            msg=data.msg,
            options=data.options,
            image_url=qr_image_url.json()['direct_url']
        )
        if converted_to_url is not None:
            res.original_msg = data.msg
            res.msg = converted_to_url

        return res
