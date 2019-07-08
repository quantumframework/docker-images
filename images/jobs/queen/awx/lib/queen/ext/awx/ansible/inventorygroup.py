from queen.lib.ansible import AnsibleModule
from ..client import AnsibleTowerClient


class InventoryGroupModule(AnsibleModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'inventory_id': {'type': 'int', 'required': True},
        'name': {'type': 'str', 'required': True},
        'description': {'type': 'str', 'required': False, 'default': ''},
        'variables': {'type': 'str', 'required': False, 'default': ''},
    }

    @property
    def inventory_id(self):
        return self.params['inventory_id']

    def setupmodule(self, *args, **kwargs):
        self.client = AnsibleTowerClient\
            .fromansibleparams(self.module.params)

    def run(self):
        query = self.client.list('inventories',
            self.inventory_id, 'groups',
            params={'name': self.params['name']})
        if not query and not self.isremoved():
            self.changed = True
            self.exit(resource=self.create())

        assert len(query) == 1
        self.resource = query[0]

        if not self.isremoved():
            self.exit(resource=self.update())

        self.delete()
        self.exit()

    def create(self):
        """Creates a new inventory group."""
        dto = {
            'name': self.params['name'],
            'description': self.params['description'],
            'variables': self.params.get('variables') or ''
        }
        response = self.client.request('POST', 'inventories',
            self.inventory_id, 'groups', json=dto)
        if response.status_code >= 400:
            self.fail(str(response.text))
        return response.json()

    def update(self):
        """Updates the inventory group."""
        dto = {
            'name': self.params['name'],
            'description': self.params['description'],
            'variables': str.strip(self.params.get('variables')) or ''
        }
        for k in dto.keys():
            if self.resource[k] != dto[k]:
                break
        else:
            return self.resource

        self.changed = True
        response = self.client.request('PUT', 'groups',
            self.resource['id'], json=dto)
        if response.status_code >= 400:
            self.fail(str(response.text))
        return response.json()

    def delete(self):
        self.changed = True
        response = self.client.request('DELETE', 'groups',
            self.resource['id'])
        if response.status_code >= 400:
            self.fail(str(response.text))
        return self.resource
