from typing import NamedTuple, TypedDict

import numpy as np
from PIL import Image
from UliEngineering.Math.Coordinates import BoundingBox
from pydantic import BaseModel

from .qr import RequestQrCode


class Point(BaseModel):
    """x y coordinates"""
    x: int
    y: int


class Layer:
    """
    Layer for overlaying images
    Takes an image, the upper left point and a mask
    """
    img: Image.Image
    upper_left: Point
    mask: Image.Image = None


class QrLocation(BaseModel):
    """
    Takes the upper left and bottom right points and allows
    generating a bounding box for it.
    """
    upper_left: Point
    bottom_right: Point

    def image_box(self) -> BoundingBox:
        ul = tuple[int, int](self.upper_left.__dict__.values())
        br = tuple[int, int](self.bottom_right.__dict__.values())
        np_array = np.asarray((ul, br))
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
