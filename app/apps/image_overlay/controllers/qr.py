import io
from urllib.parse import urlparse

from starlite import State, Partial, post
from starlite.controller import Controller

from ..library import QrGeneration
from ..models import RequestQrCode, ResponseQrCode, Size


# from ...core.library import Yourls


class QrCodeController(Controller):
    path = "/qr"
    qr = QrGeneration()

    def _is_url(self, msg: str, *, state: State) -> str:
        o = urlparse(msg)
        if o.scheme != '':
            res = state.yourls.shorten(o.geturl()).json()['shorturl']
        else:
            res = None
        return res

    @post("/")
    async def post_qr_image(self,
                            state: State,
                            data: Partial[RequestQrCode],
                            ) -> ResponseQrCode:

        converted_to_url = self._is_url(data.msg, state=state)
        output_url = converted_to_url if converted_to_url is not None else data.msg
        qr_img = self.qr.generate(output_url, data.size, options=data.options)
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
        size.x, size.y = qr_img.size
        res.size = size

        if converted_to_url is not None:
            res.original_msg = data.msg
            res.msg = converted_to_url

        return res
