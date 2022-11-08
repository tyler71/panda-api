from pydantic import BaseModel

from .qr import RequestQrCode

class RequestImageOverlay(BaseModel):
    base_image: str
    qr_msg: str
    qr_location: tuple[((int, int), (int, int))]
    qr_options: dict = None


class ResponseImageOverlay(BaseModel):
    image_url: str
