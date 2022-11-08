import base64
import binascii


def is_base64(s):
    try:
        res = base64.b64encode(base64.b64decode(s)).decode().strip() == s
        return base64.b64decode(s).decode().strip() if res else s
    except binascii.Error:
        return s
