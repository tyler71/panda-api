from os import getenv

from starlite import Starlite, get, Router, State

from apps.core import set_state_startup, logging_config

from apps.image_overlay import image_overlay_router


@get("/")
def hello_world() -> dict[str, str]:
    return {'Hello': 'World'}


image_overlay_app = Router(path="/image_overlay", route_handlers=[image_overlay_router])

latest = Router(path="", route_handlers=[hello_world,
                                         image_overlay_app])
# v1_router = Router(path="v/1", route_handlers=[hello_world, image_overlay_router])

state = State()

app = Starlite(
    route_handlers=[latest],
    on_startup=[set_state_startup],
    on_shutdown=[],
    logging_config=logging_config,
    debug=True if getenv("DEBUG", False) == "True" else False,
)
