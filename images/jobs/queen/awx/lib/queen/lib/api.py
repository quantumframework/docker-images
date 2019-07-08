import os

import requests
from requests.auth import HTTPBasicAuth


empty = object()


class BaseRestClient:
    """The base class for all RESTful API clients."""
    ResourceDoesNotExist = type('ResourceDoesNotExist', (LookupError,), {})

    @staticmethod
    def envdefault(params, key, env):
        """Return the key from the parameters or default
        to the given environment variable.
        """
        value = params.get(key)
        if value is None:
            value = os.getenv(env)
        if value is None:
            raise TypeError(f"Provide the {key} parameter or set {env}")
        return value

    @classmethod
    def fromansibleparams(cls, params, *args, **kwargs):
        raise NotImplementedError

    def __init__(self, base_url, verify=True):
        """Initialize a new :class:`BaseRestClient` instance.

        Args:
            base_url (str): specifies the base URL of the API.
                All paths are relative to this URL.
            verify (bool): indicates if X.509 sent by the server
                must be verified.
        """
        self.base_url = base_url + '/api/v2'
        self.auth = None
        self.verify = verify

    def basic_auth(self, username, password):
        """Configures HTTP basic authentication for the API
        client.

        Args:
            username (str): the username to provide to the server.
            password (str): the password to provide to the server.

        Returns:
            self
        """
        self.auth = HTTPBasicAuth(username, password)
        return self

    def detail(self, *args, **kwargs):
        """Returns a single resource from the URL specified in the
        parameters.
        """
        response = self.request('GET', *args, **kwargs)
        if response.status_code == 404:
            raise self.ResourceDoesNotExist
        resource.raise_for_status()
        return response.json()

    def list(self, *args, **kwargs):
        """Returns a collection of resources from the URL specified in the
        parameters.
        """
        response = self.request('GET', *args, **kwargs)
        response.raise_for_status()
        return self.collection_from_envelope(response, response.json())

    def request(self, method, *args, **kwargs):
        """Make a request using the specified parameters. Positional
        arguments are coerced to strings and then joined by ``/``.
        """
        url = self._make_url(self.base_url, *args)
        kwargs.setdefault('verify', self.verify)
        if self.auth is not None:
            kwargs.setdefault('auth', self.auth)
        return requests.request(method, url, **kwargs)

    def _make_url(self, *args):
        return '/'.join([str.strip(str(x), '/') for x in args]) + '/'

    def collection_from_envelope(self, response, envelope):
        raise NotImplementedError
