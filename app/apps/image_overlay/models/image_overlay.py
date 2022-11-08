from typing import NamedTuple

from pydantic import BaseModel

from .qr import RequestQrCode


class Point(BaseModel):
    x: int
    y: int


class QrLocation(BaseModel):
    upper_left: Point
    bottom_right: Point


class RequestImageOverlay(BaseModel):
    base_image: str
    qr_msg: str
    qr_location: QrLocation
    qr_options: dict = None


class ResponseImageOverlay(BaseModel):
    image_url: str
