import json

from queen.lib.ansible import AnsibleModule
from ..client import AnsibleTowerClient


class BaseAnsibleTowerModule(AnsibleModule):
    can_update = True

    def setupmodule(self, *args, **kwargs):
        self.client = AnsibleTowerClient\
            .fromansibleparams(self.module.params)

    def getsubjectresource(self):
        raise NotImplementedError

    def dtofromparams(self):
        raise NotImplementedError

    def getcreateurlparts(self):
        raise NotImplementedError

    def getupdateurlparts(self):
        raise NotImplementedError

    def getdeleteurlparts(self):
        raise NotImplementedError

    def requestforcreate(self, **params):
        dto = self.dtofromparams()
        response = self.client.request(
            *self.getcreateurlparts(), **params)
        if response.status_code == 404:
            self.fail(f"Invalid URI: {response.url}")
        elif response.status_code >= 400:
            self.fail(str(response.text))
        self.changed = True
        return response.json() if response.text\
            else self.getsubjectresource()

    def requestforupdate(self, **params):
        dto = self.dtofromparams()
        response = self.client.request(
            *self.getupdateurlparts(), **params)
        if response.status_code == 404:
            self.fail(f"Invalid URI: {response.url}")
        elif response.status_code >= 400:
            self.fail(str(response.text))
        self.changed = True
        return response.json() if response.text\
            else self.getsubjectresource()

    def requestfordelete(self, **params):
        dto = self.dtofromparams()
        response = self.client.request(
            *self.getdeleteurlparts(), **params)
        if response.status_code == 404:
            self.fail(f"Invalid URI: {response.url}")
        elif response.status_code >= 400:
            self.fail(str(response.text))
        self.changed = True
        return response.json() if response.text\
            else self.getsubjectresource()

    def run(self):
        query = self.getsubjectresource()
        if not query and not self.isremoved():
            self.exit(resource=self.create())

        if not query and self.isremoved():
            self.exit(resource=None)

        assert len(query) == 1
        self.resource = query[0]

        if not self.isremoved() and self.can_update:
            self.exit(resource=self.update())

        if self.isremoved():
            self.delete()
        self.exit()

    def create(self):
        """Creates a new inventory group."""
        dto = self.dtofromparams()
        return self.requestforcreate(json=dto)

    def update(self):
        """Updates the inventory group."""
        dto = self.dtofromparams()
        for k in dto.keys():
            if self.resource[k] != dto[k]:
                break
        else:
            return self.resource
        return self.requestforupdate(json=dto)

    def delete(self):
        self.requestfordelete()
        return self.resource
