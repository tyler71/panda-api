from pydantic import BaseModel, UUID4

from dataclasses import dataclass


@dataclass()
class Qr(BaseModel):
    id: UUID4
    size: tuple
    qr_options: dict
