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
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'organization_name': {'type': 'str', 'required': False},
        'organization_id': {'type': 'str', 'required': False},
        'kind': {'type': 'str', 'required': False},
        'name': {'type': 'str', 'required': True},
        'description': {'type': 'str', 'required': False},
        'groups': {'type': 'list', 'required': False},
        'variables': {'type': 'str', 'required': False},
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
    name = module.params['name']
    description = str.strip(module.params.get('description') or '')
    groups = module.params.get('groups') or []
    variables = module.params.get('variables') or "---\n{}"
    org_name = module.params.get('organization_name')
    org_id = module.params.get('organization_id')
    state = module.params['state']
    if not org_id and not org_name:
        module.fail_json(
            msg="Specify either organization_name or organization_id")
    if org_name:
        raise NotImplementedError

    search_filter = {'name': name, 'many': True}
    if org_id:
        search_filter['organization__id'] = org_id
    if org_name:
        search_filter['organization_name'] = org_name
    obj = rf.getresource('inventories/', **search_filter)
    dto = {
        "name": name,
        "description": description,
        "organization": org_id,
        "kind": "",
        "host_filter": None,
        "variables": variables,
        "insights_credential": None
    }

    if state == 'absent' and obj is None:
        pass
    elif state == 'absent' and obj:
        raise NotImplementedError
    elif state == 'present' and not obj:
        result['changed'] = True
        response = rf.request('POST', 'inventories/', json=dto)
        if response.status_code >= 400:
            raise Exception(response.json())
        response.raise_for_status()
        obj = response.json()
    elif state == 'present' and obj:
        cmp_keys = ['description', 'variables']
        for k in cmp_keys:
            if obj[k] != dto[k]:
                result['changed'] = True
            break
        if result['changed']:
            response = rf.request('PUT', 'inventories/' + str(obj['id']),
                json=dto)
            obj = response.json()

    module.exit_json(resource=obj, **result)


def main():
    run_module()


if __name__ == '__main__':
    main()
