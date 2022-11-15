import io
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

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.x, self.y


class Layer:
    """
    Layer for overlaying images
    Takes an image, the upper left point and a mask
    """
    img: Image.Image
    upper_left: Point
    mask: Image.Image = None

    def __add__(self, o):
        if type(o) is Layer:
            layered_image = io.BytesIO()
            upper_left = tuple[int, int](o.upper_left.__dict__.values())
            self.img.paste(o.img, upper_left, o.mask)
            self.img.save(layered_image, format="png")
            res = Layer()
            res.__dict__ = {"img": Image.open(layered_image), "upper_left": self.upper_left,
                            "mask": self.mask}
            return res

        return self


class QrLocation(BaseModel):
    """
    Takes the upper left and bottom right points and allows
    generating a bounding box for it.
    """
    upper_left: Point
    bottom_right: Point

    @property
    def box(self) -> BoundingBox:
        ul = self.upper_left.coordinates
        br = self.bottom_right.coordinates
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
