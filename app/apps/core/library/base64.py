import base64
import binascii


def is_base64(s: str) -> str:
    try:
        res = base64.b64encode(base64.b64decode(s)).decode().strip() == s
        output = base64.b64decode(s).decode().strip() if res else s
    except binascii.Error:
        output = s

    assert type(output) is str
    return output
