from pydantic import BaseModel, UUID4

from dataclasses import dataclass


class Size(BaseModel):
    x: int = 100
    y: int = 100


class RequestQrCode(BaseModel):
    msg: str
    size: Size = None
    options: dict = None
    image_url: str = None

class ResponseQrCode(BaseModel):
    msg: str
    original_msg: str = None
    size: Size = None
    options: dict = None
    image_url: str = None
