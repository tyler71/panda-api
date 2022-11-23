import datetime
import hashlib
import json
import urllib.parse

import requests
from requests import JSONDecodeError
import logging

logger = logging.getLogger()


class Yourls:
    def __init__(self, domain: str, signature: str, *, method: str = "GET", output: str = 'json'):
        self.domain = f'{domain}/yourls-api.php'
        self.signature = signature
        self.method = method
        self.nonce = None
        self.output = output

    def _get_skel(self) -> dict:
        # Build the skeleton request
        skel = {
            'format': self.output,
        }
        skel.update(self._sig_timestamp())
        return skel

    def _sig_timestamp(self) -> dict:
        # Generate the signature + timestamp for the request / short-lived requests
        dt = datetime.datetime
        present_date = dt.now()
        unix_timestamp = int(datetime.datetime.timestamp(present_date))

        # Check if nonce doesn't exist, or if it does exist, check to see if it's expired (greater than n hours)
        if self.nonce is None or unix_timestamp > (
                int(dt.timestamp(dt.fromtimestamp(self.nonce['timestamp']) + datetime.timedelta(minutes=55)))):
            res = hashlib.sha512(f'{unix_timestamp}{self.signature}'.encode())
            self.nonce = {'timestamp': unix_timestamp, 'hash': 'sha512', 'signature': res.hexdigest()}
        return self.nonce

    def _make_request(self, request: dict) -> requests.models.Response:
        # cleanup, encode, and complete the request
        cleaned_request = {k: v for (k, v) in request.items() if v is not None}
        if self.method == 'GET':
            req = urllib.parse.urlencode(cleaned_request)
            result = requests.get(f'{self.domain}?{req}')
        elif self.method == 'POST':
            result = requests.post(self.domain, data=cleaned_request)
        else:
            result = None

        if type(result) is requests.models.Response:
            try:
                result.json()
            except JSONDecodeError:
                logger.critical(f'yourls._make_request {result.content}')
        return result

    def version(self) -> requests.models.Response:
        req = self._get_skel()
        req.update({
            'action': 'version',
        })
        return self._make_request(req)

    def shorten(self, url: str, title: str = None, keyword: str = None) -> requests.models.Response:
        req = self._get_skel()
        req.update({
            'action': 'shorturl',
            'url': url,
            'title': title,
            'keyword': keyword,
        })
        return self._make_request(req)

    def expand(self, url: str) -> requests.models.Response:
        req = self._get_skel()
        req.update({
            'action': 'expand',
            'shorturl': url,
        })
        return self._make_request(req)

    def stats(self, url: str) -> requests.models.Response:
        req = self._get_skel()
        req.update({
            'action': 'url-stats',
            'shorturl': url,
        })
        return self._make_request(req)

    def server_stats(self, filter: str = None) -> requests.models.Response:
        req = self._get_skel()
        valid_filters = ("top", "bottom", "rand", "last")
        if filter is not None and filter not in valid_filters:
            raise SyntaxWarning(f'Invalid argument. Available: {valid_filters}')
        req.update({
            'action': 'stats',
            'filter': filter,
        })
        return self._make_request(req)

    def db_stats(self) -> requests.models.Response:
        req = self._get_skel()
        req.update({
            'action': 'db-stats',
        })
        return self._make_request(req)


class YourlsUpdate(Yourls):
    # https://github.com/timcrockford/yourls-api-edit-url
    def __init__(self, domain: str, signature: str, *, method: str = "GET", output: str = 'json'):
        super().__init__(domain, signature, method=method, output=output)

    def update(self, shorturl: str, url: str, title: str = None) -> requests.models.Response:
        req = self._get_skel()
        req.update({
            'action': 'update',
            'shorturl': shorturl,
            'url': url,
            'title': title,
        })
        return self._make_request(req)

    def geturl(self, url: str, *, exactly_once: bool = None) -> requests.models.Response:
        req = self._get_skel()
        req.update({
            'action': 'geturl',
            'url': url,
            'exactly_once': exactly_once,
        })
        return self._make_request(req)

    # Panda-API
    # Override shorten
    def shorten(self, url: str, title: str = None, keyword: str = None) -> requests.models.Response:
        req = self._get_skel()
        req.update({
            'action': 'shorturl',
            'url': url,
            'title': title,
            'keyword': keyword,
        })
        res = self._make_request(req)

        r_json = json.loads(res.content)
        r_json['url']['update_token'] = self.generate_token(r_json['url']['keyword'], r_json['url']['date'],
                                                            r_json['url']['ip'])

        res.__dict__['_content'] = json.dumps(r_json).encode()

        return res

    def token_update_url(self, shorturl, token, new_url, new_title=None, *, hash_method=None) -> bool:
        verified = self.verify_token(shorturl, token)
        if verified:
            self.update(shorturl, new_url, new_title)
        return verified

    def verify_token(self, shorturl, token) -> bool:
        """
        Takes provided hash or token, and compares it to server
        Hash should be of <timestamp><ip><shorturl>
        """
        req = self.stats(shorturl)
        if req.status_code == 200:
            info = req.json()
            timestamp = info['link']['timestamp']
            ip = info['link']['ip']

            return self.generate_token(shorturl, timestamp, ip) == token
        else:
            logging.critical(f"yourls verify_token: {req.content}")

    def generate_token(self, shorturl, timestamp, ip, hash_method="sha1") -> str:
        hash_methods = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha512': hashlib.sha512,

        }
        res = hash_methods[hash_method](f'{timestamp}{ip}{shorturl}'.encode())
        return res.hexdigest()


class YourlsDelete(Yourls):
    # https://github.com/claytondaley/yourls-api-delete
    def __init__(self, domain: str, signature: str, *, method: str = "GET", output: str = 'json'):
        super().__init__(domain, signature, method=method, output=output)

    def delete(self, shorturl: str) -> requests.models.Response:
        req = self._get_skel()
        req.update({
            'action': 'delete',
            'shorturl': shorturl,
        })
        return self._make_request(req)


class AllYourls(YourlsDelete, YourlsUpdate):
    def __init__(self, domain: str, signature: str, *, method: str = "GET", output: str = 'json'):
        super().__init__(domain, signature, method=method, output=output)
