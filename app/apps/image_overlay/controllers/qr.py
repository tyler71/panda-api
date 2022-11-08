import base64
import binascii
from typing import Optional
from urllib.parse import urlparse

from starlite import State, Partial, get, post
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

    def _is_base64(self, s):
        try:
            res = base64.b64encode(base64.b64decode(s)).decode().strip() == s
            return base64.b64decode(s).decode().strip() if res else s
        except binascii.Error:
            return s

    @get("/{msg:str}")
    async def get_qr_image(self,
                           state: State,
                           msg: str,
                           size: Optional[Size] = None,
                           options: Optional[dict] = None,
                           ) -> ResponseQrCode:
        msg = self._is_base64(msg)
        converted_to_url = self._is_url(msg, state=state)
        img = self.qr.generate(msg, size, options=options)
        image_url = 'https://demo.img'

        res = QrCode(
            msg=msg,
            size=size,
            options=options,
            image_url=image_url
        )
        if converted_to_url is not None:
            res.original_msg = msg
            res.msg = converted_to_url
        return res

    @post("/")
    async def post_qr_image(self,
                            state: State,
                            data: Partial[RequestQrCode],
                            ) -> ResponseQrCode:

        converted_to_url = self._is_url(data.msg, state=state)
        qr_img = self.qr.generate(data.msg, data.size, options=data.options)
        image_url = 'https://demo.img'

        res = ResponseQrCode(
            msg=data.msg,
            options=data.options,
            image_url=image_url
        )
        size = Size()
        size.x, size.y = qr_img.size
        res.size = size

        if converted_to_url is not None:
            res.original_msg = data.msg
            res.msg = converted_to_url

        return res
