from pydantic import BaseModel, UUID4

from dataclasses import dataclass


@dataclass()
class Size(BaseModel):
    x: int = 100
    y: int = 100


class QrCode(BaseModel):
    id: UUID4
    msg: str
    original_msg: str = None
    size: Size = None
    options: dict = None
    image_url: str = None
