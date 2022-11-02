from urllib.parse import urlparse

from pydantic import BaseModel
from starlite import State
from starlite.controller import Controller
from starlite.handlers import get

from ..library import QrGeneration


# from ...core.library import Yourls

class QrCode(BaseModel):
    id: int
    msg: str
    size: tuple
    options: dict
    image_url: str


def _is_url(msg: str, *, state: State):
    o = urlparse(msg)
    if o.scheme != '':
        res = state.yourls.shorten(o.geturl())
    else:
        res = msg
    return res


class QrCodeController(Controller):
    path = "/qr"
    qr = QrGeneration()

    @get("/")
    async def get_qr_image(self, data: QrCode) -> QrCode:
        _is_url(data.msg)
        return QrCode

