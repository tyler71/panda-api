import uuid
from typing import Optional
from urllib.parse import urlparse

from starlite import State, Partial, get, post
from starlite.controller import Controller

from ..library import QrGeneration
from ..models import QrCode, Size


# from ...core.library import Yourls


class QrCodeController(Controller):
    path = "/qr"
    qr = QrGeneration()

    def _is_url(self, msg: str, *, state: State) -> str:
        o = urlparse(msg)
        if o.scheme != '':
            res = state.yourls.shorten(o.geturl())
        else:
            res = None
        return res

    @get("/{msg:str}")
    async def get_qr_image(self,
                           state: State,
                           msg: str,
                           size: Optional[Size] = None,
                           options: Optional[dict] = None,
                           ) -> QrCode:
        converted_to_url = self._is_url(msg, state=state)
        self.qr.generate(msg, size, options=options)
        image_url = 'https://demo.img'

        res = QrCode(
            id=uuid.uuid4(),
            msg=msg,
            size=size,
            options=options,
            image_url=image_url
        )
        if converted_to_url is None:
            res.original_msg = msg
            res.msg = converted_to_url
        return res

    @post("/")
    async def post_qr_image(self,
                            state: State,
                            data: Partial[QrCode],
                            ) -> QrCode:

        converted_to_url = self._is_url(data.msg, state=state)
        self.qr.generate(data.msg, data.size, options=data.options)
        image_url = 'https://demo.img'

        res = QrCode(
            msg=data.msg,
            size=data.size,
            options=data.options,
            image_url=image_url
        )
        if converted_to_url is not None:
            res.original_msg = data.msg
            res.msg = converted_to_url.json()['shorturl']
        print(data)
        return res
