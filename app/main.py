from starlite import Starlite, get


@get("/")
def hello_world() -> dict[str, str]:
    """Handler function that returns a greeting dictionary."""
    a = 5 + 2
    return {"hello": "world"}


app = Starlite(route_handlers=[hello_world])

