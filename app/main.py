import os
import uvicorn
from starlite import Starlite, get
from functools import partial


@get("/")
def hello_world() -> dict[str, str]:
    """Handler function that returns a greeting dictionary."""
    a = 5 + 2
    return {"hello": "world"}


app = Starlite(route_handlers=[hello_world])

if __name__ == "__main__":
    debug_mode = True if os.getenv("DEBUG", False) == "True" else False
    server_config = uvicorn.Config(
        app="main:app",
        host="0.0.0.0",
        port=os.getenv("PORT", 8000),
        reload=debug_mode,
        reload_dirs=["/app"])
    server = uvicorn.Server(server_config)
    server.run()
