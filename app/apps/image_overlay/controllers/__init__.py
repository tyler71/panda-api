from starlite import Router

from .qr import QrCodeController
from .image_overlay import ImageOverlayController

image_overlay_router = Router(path="", route_handlers=[QrCodeController,
                                                       ImageOverlayController,
                                                       ])
