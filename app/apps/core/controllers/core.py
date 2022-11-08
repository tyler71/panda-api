from pydantic import BaseSettings
from starlite import State

from .startup_down import get_yourls_connection, get_linx_connection


class AppSettings(BaseSettings):
    YOURLS_DOMAIN: str
    YOURLS_SIGNATURE: str
    LINX_DOMAIN: str
    LINX_APIKEY: str

    class Config:
        case_sensitive = True


settings = AppSettings()


def set_state_startup(state: State):
    state.settings = settings
    state.yourls = get_yourls_connection(state=state, domain=settings.YOURLS_DOMAIN,
                                         signature=settings.YOURLS_SIGNATURE)
    state.linx = get_linx_connection(state=state, domain=settings.LINX_DOMAIN, apikey=settings.LINX_APIKEY)
