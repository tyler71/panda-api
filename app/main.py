from starlite import Starlite, get, State

from apps.core.controllers.core import set_state_startup

from apps.image_overlay.controllers.qr import QrCodeController


@get("/")
def hello_world() -> dict[str, str]:
    return {'Hello': 'World'}


app = Starlite(
    route_handlers=[hello_world, QrCodeController],
    on_startup=[set_state_startup],
    on_shutdown=[],
    debug=True,
)
