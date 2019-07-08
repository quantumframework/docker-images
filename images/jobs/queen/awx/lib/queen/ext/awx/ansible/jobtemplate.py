from .base import BaseAnsibleTowerModule


class JobTemplateModule(BaseAnsibleTowerModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'inventory_id': {'type': 'int', 'required': True},
        'project_id': {'type': 'int', 'required': True},
        'kind': {'type': 'str', 'required': True},
        'name': {'type': 'str', 'required': True},
        'playbook': {'type': 'str', 'required': True},

        'description': {'type': 'str', 'required': False, 'default': ''},
        'variables': {'type': 'str', 'required': False, 'default': ''}, # extra_vars
        'become': {'type': 'bool', 'required': False, 'default': False},
        'forks': {'type': 'int', 'required': False, 'default': 0},
        'host_pattern': {'type': 'str', 'required': False, 'default': ''},
        'verbosity': {'type': 'int', 'required': False, 'default': 0},
        'tags': {'type': 'str', 'required': False, 'default': ''},
        'skip': {'type': 'str', 'required': False, 'default': ''},
        'force_handlers': {'type': 'bool', 'required': False, 'default': False},
        'timeout': {'type': 'int', 'required': False, 'default': 120},
        'use_fact_cache': {'type': 'bool', 'required': False, 'default': False},
        'show_diff': {'type': 'bool', 'required': False, 'default': False},
        'concurrent': {'type': 'bool', 'required': False, 'default': False},
        'job_slice_count': {'type': 'int', 'required': False, 'default': 1},
    }

    def dtofromparams(self):
        return {
            'inventory': self.params['inventory_id'],
            'project': self.params['project_id'],
            'name': self.params['name'],
            'description': self.params['description'],
            'job_type': self.params['kind'],
            'become_enabled': self.params['become'],
            'extra_vars': self.params['variables'],
            'playbook': self.params['playbook'],
            'forks': self.params['forks'],
            'limit': self.params['host_pattern'],
            'verbosity': self.params['verbosity'],
            'job_tags': self.params['tags'],
            'skip_tags': self.params['skip'],
            'force_handlers': self.params['force_handlers'],
            'start_at_task': "",
            'timeout': self.params['timeout'],
            'use_fact_cache': self.params['use_fact_cache'],
            'host_config_key': "",
            'survey_enabled': False,
            'diff_mode': self.params['show_diff'],
            'allow_simultaneous': self.params['concurrent'],
            'custom_virtualenv': None,
            'job_slice_count': self.params['job_slice_count'],
            'ask_diff_mode_on_launch': False,
            'ask_variables_on_launch': False,
            'ask_limit_on_launch': False,
            'ask_tags_on_launch': False,
            'ask_skip_tags_on_launch': False,
            'ask_job_type_on_launch': False,
            'ask_verbosity_on_launch': False,
            'ask_inventory_on_launch': False,
            'ask_credential_on_launch': False
        }

    def getsubjectresource(self):
        return self.client.list('job_templates', params={
            'name': self.params['name']
        })

    def getcreateurlparts(self):
        return ['POST', 'job_templates']

    def getupdateurlparts(self):
        return ['PUT', 'job_templates', self.resource['id']]

    def getdeleteurlparts(self):
        return ['DELETE', 'job_templates', self.resource['id']]
