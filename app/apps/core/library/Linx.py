import base64
import io
import logging
import urllib.parse

import requests
from requests import JSONDecodeError


class Skel:
    request: dict = dict()
    headers: dict = dict()
    endpoint: str
    method: str


logger = logging.getLogger()


class Linx:
    def __init__(self, domain: str, apikey: str):
        self.domain = domain
        self.apikey = apikey
        self.qp = urllib.parse.quote_plus

    def _get_skel(self) -> Skel:
        # Build the skeleton request
        skel = Skel()
        skel.headers.update({
            'Linx-Api-Key': self.apikey,
            'Accept': 'application/json',
            'User-Agent': 'panda-api',
        })

        return skel

    def _auth_header(self) -> str:

        sample_string = base64.b64encode(self.apikey)
        sample_string_bytes = sample_string.encode("ascii")

        base64_bytes = sample_string_bytes

    def _make_request(self, req: Skel) -> requests.models.Response:
        # cleanup, encode, and complete the request
        if type(req.request) == dict:
            req.request = {k: v for (k, v) in req.request.items() if v is not None}
        if type(req.headers) == dict:
            req.headers = {k: v for (k, v) in req.headers.items() if v is not None}

        if req.method == 'GET':
            result = requests.get(f'{self.domain}{req.endpoint}/{req.request}', headers=req.headers)
        elif req.method == 'POST':
            result = requests.post(f'{self.domain}{req.endpoint}', data=req.request, headers=req.headers)
        elif req.method == 'PUT':
            result = requests.put(f'{self.domain}{req.endpoint}', data=req.request, headers=req.headers)
        elif req.method == 'DELETE':
            result = requests.delete(f'{self.domain}{req.endpoint}', headers=req.headers)
        else:
            result = None

        if type(result) is requests.models.Response:
            try:
                result.json()
            except JSONDecodeError:
                logger.critical(f'yourls._make_request {result.content}')
        return result

    def upload(self, file, filename: str = None, randomize_filename: bool = None, delete_key: str = None,
               password: str = None, expiration_seconds: int = None):
        req = self._get_skel()
        req.headers.update({
            'Linx-Randomize': 'yes' if randomize_filename else None,
            'Linx-Delete-Key': delete_key,
            'Linx-Access-Key': password,
            'Linx-Expiry': str(expiration_seconds),
            'Content-Disposition': f'attachment; filename={filename}'
        })

        filename = self.qp(filename) if filename is not None else filename

        req.method = 'PUT'
        req.endpoint = f'/upload/{filename}'
        req.request = file
        return self._make_request(req)

    def overwrite(self, file: io.BytesIO, delete_key: str) -> requests.models.Response:
        req = self._get_skel()
        req.headers.update({
            'Linx-Delete-Key': delete_key,
        })
        req.method = 'POST'
        req.endpoint = '/upload'
        req.request = file
        return self._make_request(req)

    def delete(self, filename: str, delete_key: str) -> requests.models.Response:
        req = self._get_skel()
        req.headers.update({
            'Linx-Delete-Key': delete_key,
        })
        req.method = 'DELETE'
        req.endpoint = f'/{self.qp(filename)}'
        return self._make_request(req)

    def info(self, filename: str) -> requests.models.Response:
        req = self._get_skel()
        req.method = 'GET'
        req.endpoint = f'/{self.qp(filename)}'
        return self._make_request(req)
