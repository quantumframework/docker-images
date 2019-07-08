from .base import BaseAnsibleTowerModule


class JobTemplateCredentialModule(BaseAnsibleTowerModule):
    can_update = False
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'job_template_id': {'type': 'int', 'required': True},
        'credential_id': {'type': 'int', 'required': True},
    }

    @property
    def job_id(self):
        return self.params['job_template_id']

    def getsubjectresource(self):
        return self.client.list('job_templates', self.job_id,
            'credentials', params={'id': self.params['credential_id']})

    def dtofromparams(self):
        dto = {'id': self.params['credential_id']}
        if self.isremoved():
            dto['disassociate'] = True
        return dto

    def getcreateurlparts(self):
        return ['POST', 'job_templates', self.job_id, 'credentials']

    def getdeleteurlparts(self):
        return ['POST', 'job_templates', self.job_id, 'credentials']

    def requestfordelete(self, *args, **kwargs):
        return self.requestforcreate(*args, **kwargs)
