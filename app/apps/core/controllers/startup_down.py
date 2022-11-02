from typing import cast

from starlite import State

from ..library import Yourls

def get_yourls_connection(state: State, domain: str, signature:str, method: str = 'POST', output: str = 'json') -> Yourls:
    if not getattr(state, "yourls", None):
        state.yourls = Yourls(domain=domain, signature=signature, method=method, output=output)
    return cast("Yourls", state.yourls)