from typing import cast

from starlite import State

from ..library import Yourls, Linx


def get_yourls_connection(state: State, domain: str, signature: str, method: str = 'POST',
                          output: str = 'json') -> Yourls:
    if not getattr(state, "yourls", None):
        state.yourls = Yourls(domain=domain, signature=signature, method=method, output=output)
    return cast("Yourls", state.yourls)


def get_linx_connection(state: State, domain: str, apikey: str) -> Linx:
    if not getattr(state, "linx", None):
        state.linx = Linx(domain=domain, apikey=apikey)
    return cast("Linx", state.linx)
