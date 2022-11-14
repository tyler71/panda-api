from urllib.parse import urlparse

from requests import JSONDecodeError, Request
from starlite import State


def try_shorten_url(msg: str, *, state: State, request: Request) -> str:
    o = urlparse(msg)
    if o.scheme != '':
        res = state.yourls.shorten(o.geturl())
    else:
        res = None
    return res
