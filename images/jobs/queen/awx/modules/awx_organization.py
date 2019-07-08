import os

import requests
from ansible.module_utils.basic import AnsibleModule
from requests.auth import HTTPBasicAuth


def run_module():
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'name': {'type': 'str', 'required': True},
        'description': {'type': 'str', 'required': False, 'default': ''},
        'max_hosts': {'type': 'int', 'required': False, 'default': 0},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
    }
    result = {
        'changed': False
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)
        return

    new = False
    state = module.params.get('state')
    must_create = state == 'present'
    must_remove = state == 'absent'
    must_verify_x509 = bool(module.params.get('validate_certs'))
    base_url = module.params.get('api_url')\
        or os.getenv('AWX_URL')
    user = module.params.get('api_user') or os.getenv('AWX_USER')
    password = module.params.get('api_password') or os.getenv('AWX_PASSWORD')
    if not base_url:
        module.fail_json(
            msg="Provide the api_url argument or set the AWX_URL "
                "environment variable.",
            **result
        )
        return
    if not user:
        module.fail_json(
            msg="Provide the api_user argument or set the AWX_USER "
                "environment variable.",
            **result
        )
        return
    if not password:
        module.fail_json(
            msg="Provide the api_password argument or set the AWX_PASSWORD "
                "environment variable.",
            **result
        )
        return

    auth = HTTPBasicAuth(user, password)

    # Get the organization details. If it doesn't exist, then this
    # is a create operation.
    response = requests.get(
        base_url + '/api/v2/organizations/?name=' + module.params['name'],
        auth=auth, verify=must_verify_x509)
    dto = response.json()
    org = None

    if dto['count'] == 0:
        new = True
    else:
        org = dto['results'][0]

    if must_create:
        # Create a new Organization.
        dto = {
            'name': module.params['name'],
            'description': module.params['description'],
            'max_hosts': module.params['max_hosts']
        }
        if new:
            response = requests.post(base_url + '/api/v2/organizations/',
                auth=auth, verify=must_verify_x509, json=dto)
            response.raise_for_status()
            result['changed'] = True
            org = response.json()
        else:
            assert org
            for k in set(dto.keys()):
                # Strip string because unexpected newlines from YAML
                # input.
                if str(dto[k]).strip() == str(org[k]):
                    continue
                result['changed'] = True
                response = requests.put(base_url + '/api/v2/organizations/' + str(org['id']) + '/',
                    auth=auth, verify=must_verify_x509, json=dto)
                response.raise_for_status()
                org = response.json()
                break

    if org and must_remove and not new:
        result['changed'] = True
        url = base_url + '/api/v2/organizations/' + str(org['id'])
        response = requests.delete(url, auth=auth, verify=must_verify_x509)
        response.raise_for_status()
        result['changed'] = True

    module.exit_json(org=org, **result)


def main():
    run_module()


if __name__ == '__main__':
    main()
