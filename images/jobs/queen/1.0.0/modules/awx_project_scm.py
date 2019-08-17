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
        'organization_id': {'type': 'int', 'required': False},
        'name': {'type': 'str', 'required': True},
        'description': {'type': 'str', 'required': False},
        'credential': {'type': 'int', 'required': False},
        'scm_type': {'type': 'str', 'required': True},
        'scm_url': {'type': 'str', 'required': True},
        'scm_branch': {'type': 'str', 'required': True},
        'scm_delete_on_update': {'type': 'bool', 'required': False},
        'scm_clean': {'type': 'bool', 'required': False, 'default': False},
        'scm_update_on_launch': {'type': 'bool', 'required': False},
        'scm_update_cache_timeout': {'type': 'int', 'required': False, 'default': 0},
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
    org_name = module.params.get('organization_name')
    org_id = module.params.get('organization_id')
    if not org_id and not org_name:
        module.fail_json(
            msg="Specify either organization_name or organization_id")
    if org_name:
        raise NotImplementedError

    state = module.params['state']
    name = module.params['name']
    description = str.strip(module.params.get('description') or '')
    scm_type = module.params['scm_type']
    scm_url = module.params['scm_url']
    scm_branch = module.params['scm_branch']
    scm_delete_on_update = bool(module.params.get('scm_delete_on_update'))
    scm_update_on_launch = bool(module.params.get('scm_update_on_launch'))
    scm_update_cache_timeout = module.params['scm_update_cache_timeout']
    scm_clean = module.params['scm_clean']

    search_filter = {'name': name, 'many': True}
    if org_id:
        search_filter['organization__id'] = org_id
    if org_name:
        search_filter['organization_name'] = org_name
    obj = rf.getresource('projects/', **search_filter)
    dto = {
        "organization": org_id,
        "name": name,
        "description": description,
        "scm_type": scm_type,
        "scm_url": scm_url,
        "scm_branch": scm_branch,
        "scm_delete_on_update": scm_delete_on_update,
        "scm_update_on_launch": scm_update_on_launch,
        "scm_update_cache_timeout": scm_update_cache_timeout,
        'scm_clean': scm_clean
    }
    if module.params.get('credential'):
        dto['credential'] = module.params['credential']

    if state == 'absent' and obj is None:
        pass
    elif state == 'absent' and obj:
        raise NotImplementedError
    elif state == 'present' and not obj:
        result['changed'] = True
        response = rf.request('POST', 'projects/', json=dto)
        if response.status_code >= 400:
            raise Exception(response.json())
        response.raise_for_status()
        obj = response.json()
    elif state == 'present' and obj:
        payload = {}
        for k in dto.keys():
            if obj[k] == dto[k]:
                continue
            result['changed'] = True
            payload[k] = dto[k]
        if result['changed']:
            response = rf.request('PATCH', 'projects/' + str(obj['id']) + '/',
                json=dto)
            if response.status_code >= 400:
                raise Exception(response.text, dto)
            obj = response.json()

    module.exit_json(resource=obj, **result)


def main():
    run_module()


if __name__ == '__main__':
    main()

