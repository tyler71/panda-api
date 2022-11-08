from typing import NamedTuple

from pydantic import BaseModel

from .qr import RequestQrCode


class Point(BaseModel):
    x: int
    y: int


class QrLocation(BaseModel):
    upper_left: Point
    bottom_right: Point


class QrImageOverlay(BaseModel):
    msg: str
    location: QrLocation
    options: dict = None
    background_url: str = None


class RequestImageOverlay(BaseModel):
    base_image: str
    qr: QrImageOverlay


class ResponseImageOverlay(BaseModel):
    image_url: str
