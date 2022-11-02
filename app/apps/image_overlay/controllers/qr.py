from typing import List

from pydantic import UUID4
from starlite import Controller, Partial, get, post, put, patch, delete

from ..models import Qr

