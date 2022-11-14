from urllib.parse import urlparse

from requests import JSONDecodeError, Request
from starlite import State

import logging

logger = logging.getLogger()


def try_shorten_url(msg: str, *, state: State, request: Request) -> str:
    o = urlparse(msg)
    if o.scheme != '':
        response = state.yourls.shorten(o.geturl())
        try:
            output = response.json()['shorturl']
        except JSONDecodeError:
            logger.critical(f'yourls._make_request {response.content}')
    else:
        output = None

    assert type(output) is str, f'try_shorten_url: output must be a str, not {output}'
    return output
