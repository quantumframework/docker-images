import os

import requests
from ansible.module_utils.basic import AnsibleModule
from requests.auth import HTTPBasicAuth



class RequestFactory:

    @classmethod
    def fromansibleparams(cls, params):
        return cls(
            params.get('api_url') or os.getenv('AWX_URL'),
            params.get('api_user') or os.getenv('AWX_USER'),
            params.get('api_password') or os.getenv('AWX_PASSWORD'),
            bool(params.get('validate_certs'))
        )

    def __init__(self, base_url, username, password, validate_certs=True):
        self.base_url = base_url + '/api/v2'
        self.username = username
        self.password = password
        self.auth = HTTPBasicAuth(self.username, self.password)
        self.validate_certs = validate_certs

    def request(self, method, url, *args, **kwargs):
        kwargs.setdefault('verify', self.validate_certs)
        kwargs.setdefault('auth', self.auth)
        return requests.request(method, '/'.join([self.base_url, url]),
            *args, **kwargs)

    def getresource(self, url, **params):
        """Returns the resource matching the parameters,
        or ``None``.
        """
        many = params.pop('many', False)
        response = self.request('GET', url, params=params)
        response.raise_for_status()
        envelope = response.json()
        if not many:
            return response.json()

        return envelope['results'][0] if envelope['results']\
            else None


def run_module():
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'organization_name': {'type': 'str', 'required': False},
        'organization_id': {'type': 'str', 'required': False},
        'kind': {'type': 'str', 'required': True},
        'name': {'type': 'str', 'required': True},
        'username': {'type': 'str', 'required': False},
        'description': {'type': 'str', 'required': False},
        'key': {'type': 'str', 'required': True},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
    }
    result = {
        'changed': False
    }
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Setup the local scope.
    rf = RequestFactory.fromansibleparams(module.params)
    kind = module.params['kind']
    key = module.params['key']
    username = str.strip(module.params.get('username') or '')
    name = module.params['name']
    description = str.strip(module.params.get('description') or '')
    org_name = module.params.get('organization_name')
    org_id = module.params.get('organization_id')
    state = module.params['state']
    credential = rf.getresource('credentials/',
        name=module.params['name'],
        credential_type__kind=kind,
        many=True)
    credential_type = rf.getresource('credential_types',
        kind=kind, many=True)

    if not org_id and not org_name:
        module.fail_json(
            msg="Specify either organization_name or organization_id")
    if org_name:
        raise NotImplementedError

    dto = {
        'credential_type': credential_type['id'],
        'organization': org_id,
        'name': name,
        'inputs': {
            'ssh_key_data': key
        }
    }
    if description:
        dto['description'] = description
    if username:
        dto['inputs']['username'] = username

    if state == 'absent' and credential is None:
        pass
    elif state == 'absent' and credential:
        raise NotImplementedError
    elif state == 'present' and not credential:
        result['changed'] = True
        response = rf.request('POST', 'credentials/', json=dto)
        if response.status_code >= 400:
            raise Exception(response.json())
        response.raise_for_status()
        credential = response.json()
    elif state == 'present' and credential:
        pass

    module.exit_json(resource=credential, **result)


def main():
    run_module()


if __name__ == '__main__':
    main()
