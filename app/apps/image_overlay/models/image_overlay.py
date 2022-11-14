from typing import NamedTuple, TypedDict

import numpy as np
from PIL import Image
from UliEngineering.Math.Coordinates import BoundingBox
from pydantic import BaseModel

from .qr import RequestQrCode


class Point(BaseModel):
    x: int
    y: int


class Layer:
    img: Image.Image
    upper_left: Point
    mask: Image.Image = None


class QrLocation(BaseModel):
    upper_left: Point
    bottom_right: Point

    def image_box(self) -> BoundingBox:
        ulx, uly, brx, bry = int(self.upper_left.x), int(self.upper_left.y), int(self.bottom_right.x),\
                             int(self.bottom_right.y)
        np_array = np.asarray(((ulx, uly), (brx, bry)))
        box = BoundingBox(np_array)
        return box


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
