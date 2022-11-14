from pydantic import BaseSettings
from starlite import State, LoggingConfig

from .startup_down import get_yourls_connection, get_linx_connection


class AppSettings(BaseSettings):
    YOURLS_DOMAIN: str
    YOURLS_SIGNATURE: str
    LINX_DOMAIN: str
    LINX_APIKEY: str
    QR_IMAGE_EXPIRATION: int = 86400

    class Config:
        case_sensitive = True


logging_config = LoggingConfig(
    loggers={
        "panda-api": {
            "level": "INFO",
            "handlers": ["queue_listener"],
        }
    }
)


def set_state_startup(state: State):
    settings = AppSettings()
    state.settings = settings
    state.yourls = get_yourls_connection(state=state, domain=settings.YOURLS_DOMAIN,
                                         signature=settings.YOURLS_SIGNATURE)
    state.linx = get_linx_connection(state=state, domain=settings.LINX_DOMAIN, apikey=settings.LINX_APIKEY)
