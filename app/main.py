from starlite import Starlite, Router, get
from pydantic import BaseModel

class User(BaseModel):
    Name: str

@get("/")
def hello_world() -> dict[str, str]:
    """Handler function that returns a greeting dictionary."""
    a = 5 + 2
    return {"hello": "world"}

@get("/{user_id:int}")
def get_user(user_id: int) -> dict[str, str]:
    return {str(user_id): f"hi {user_id}"}


user_router = Router(path="/user", route_handlers=[get_user])

app = Starlite(route_handlers=[hello_world, user_router])