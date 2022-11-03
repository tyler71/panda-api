from urllib.parse import urlparse
from typing import Optional

import uuid
from pydantic import BaseModel, UUID4
from starlite import State, get, Parameter
from starlite.controller import Controller

from ..library import QrGeneration


# from ...core.library import Yourls

class Size(BaseModel):
    x: int
    y: int

class QrCode(BaseModel):
    id: UUID4
    msg: str
    size: Size = None
    options: dict = None
    image_url: str




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
                           size: Optional[Size] = Parameter(default={'x': 100, 'y': 100}),
                           options: Optional[dict] = Parameter(query="qrOptions"),
    ) -> QrCode:
        print(state, msg, size, options)
        converted_to_url = self._is_url(msg, state=state)
        self.qr.generate(msg, size, options=options)
        image_url = 'https://demo.img'

        res = QrCode(
            id = uuid.uuid4(),
            msg = msg,
            size = size,
            options = options,
            image_url = image_url
        )
        if converted_to_url is not None:
            res.original_msg = msg
            res.msg = converted_to_url
        return res

