from queen.lib.api import BaseRestClient


class AnsibleTowerClient(BaseRestClient):

    @classmethod
    def fromansibleparams(cls, params, *args, **kwargs):
        client = cls(
            AnsibleTowerClient.envdefault(params, 'api_url', 'AWX_URL'),
            AnsibleTowerClient.envdefault(params, 'validate_certs', 'AWX_VALIDATE_CERTS'),
        )
        return client.basic_auth(
            AnsibleTowerClient.envdefault(params, 'api_user', 'AWX_USER'),
            AnsibleTowerClient.envdefault(params, 'api_password', 'AWX_PASSWORD'),
        )

    def collection_from_envelope(self, response, envelope):
        return envelope['results']\
            if bool(envelope.get('count'))\
            else []
