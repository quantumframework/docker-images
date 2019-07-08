from .base import BaseAnsibleTowerModule


class InventoryHostModule(BaseAnsibleTowerModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'inventory_id': {'type': 'int', 'required': False},
        'group_id': {'type': 'int', 'required': False},
        'host': {'type': 'str', 'required': True}, # name in API
        'description': {'type': 'str', 'required': False, 'default': ''},
        'variables': {'type': 'str', 'required': False, 'default': ''},
        'enabled': {'type': 'bool', 'required': False, 'default': False},
    }

    @property
    def inventory_id(self):
        return self.params['inventory_id']

    @property
    def group_id(self):
        return self.params['group_id']

    def getsubjectresource(self):
        if self.inventory_id:
            return self.client.list('hosts',
                params={'name': self.params['host']})
        if self.group_id:
            return self.client.list('groups', self.group_id, 'hosts',
                params={'name': self.params['host']})

        raise NotImplementedError

    def dtofromparams(self):
        dto = {
            'name': self.params['host'],
            'description': self.params['description'],
            'variables': str.strip(self.params.get('variables') or ''),
            'enabled': self.params['enabled']
        }
        if self.params.get('inventory_id'):
            dto['inventory'] = self.params['inventory_id']
        return dto

    def getcreateurlparts(self):
        inventory_id = self.params.get('inventory_id')
        group_id = self.params.get('group_id')
        if not inventory_id and not group_id\
        or inventory_id and group_id:
            self.fail("Specify either inventory_id or group_id")
        args = ['POST']
        if inventory_id:
            args.append('hosts')
        elif group_id:
            args.append('groups')
            args.append(group_id)
            args.append('hosts')
        return args

    def getupdateurlparts(self):
        return ['PUT', 'hosts', self.resource['id']]

    def getdeleteurlparts(self):
        args = ['DELETE']
        args.append('hosts')
        args.append(self.resource['id'])
        return args
