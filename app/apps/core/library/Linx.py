import io

import requests


class Skel:
    request: dict = dict()
    headers: dict = dict()
    endpoint: str
    method: str


class Linx:
    def __init__(self, domain: str, apikey: str):
        self.domain = domain
        self.apikey = apikey

    def _get_skel(self) -> Skel:
        # Build the skeleton request
        skel = Skel()
        skel.headers.update({
            'Linx-Api-Key': self.apikey,
            'Accept': 'application/json',
        })

        return skel

    def _make_request(self, req: Skel) -> requests.models.Response:
        # cleanup, encode, and complete the request
        if type(req.request) == dict:
            req.request = {k: v for (k, v) in req.request.items() if v is not None}
        if type(req.headers) == dict:
            req.headers = {k: v for (k, v) in req.headers.items() if v is not None}
        if req.method == 'GET':
            result = requests.get(f'{self.domain}{req.endpoint}{req.request}', headers=req.headers)
        elif req.method == 'POST':
            result = requests.post(f'{self.domain}{req.endpoint}', files=req.request, headers=req.headers)
        elif req.method == 'PUT':
            result = requests.put(f'{self.domain}{req.endpoint}', files=req.request, headers=req.headers)
            print(requests.Request('PUT', self.domain, files=req.request).prepare().body)
        elif req.method == 'DELETE':
            result = requests.delete(f'{self.domain}{req.endpoint}', headers=req.headers)
        else:
            result = None
        return result

    def upload(self, file: io.BytesIO, filename: str = None, content_type=None, randomize_filename: bool = None,
               delete_key: str = None,
               password: str = None, expiration_seconds: int = None):
        req = self._get_skel()
        req.headers.update({
            'Linx-Randomize': 'yes' if randomize_filename else None,
            'Linx-Delete-Key': delete_key,
            'Linx-Access-Key': password,
            'Linx-Expiry': str(expiration_seconds),
        })

        req.method = 'PUT'
        req.endpoint = f'/upload/{filename}'
        req.request = {'files': (filename, file, content_type)}
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
        req.endpoint = f'/{filename}'
        return self._make_request(req)

    def info(self, filename: str) -> requests.models.Response:
        req = self._get_skel()
        req.method = 'GET'
        req.endpoint = f'/{filename}'
        return self._make_request(req)

