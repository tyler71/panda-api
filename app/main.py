from starlite import Starlite, get, Router

from apps.core.controllers.core import set_state_startup

from apps.image_overlay.controllers import image_overlay_router


@get("/")
def hello_world() -> dict[str, str]:
    return {'Hello': 'World'}


latest = Router(path="", route_handlers=[hello_world, image_overlay_router])
# v1 = Router(path="/v1", route_handlers=[hello_world, image_overlay_router])

app = Starlite(
    route_handlers=[latest],
    on_startup=[set_state_startup],
    on_shutdown=[],
    debug=True,
)
