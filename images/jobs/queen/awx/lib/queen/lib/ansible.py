import ansible.module_utils.basic


class AnsibleModule:
    """The base class for all Quantum Queen Ansible modules."""
    supports_check_mode = False

    @property
    def params(self):
        return self.module.params

    def __init__(self, *args, **kwargs):
        self.module = ansible.module_utils.basic.AnsibleModule(
            argument_spec=self.getparameters(),
            supports_check_mode=self.supports_check_mode
        )
        self.changed = False
        self.setupmodule(*args, **kwargs)

    def getparameters(self):
        """Return the parameters for the Ansible module."""
        return self.module_args

    def setupmodule(self, *args, **kwargs):
        """Set up the Ansible module object state."""
        pass

    def handle(self):
        return self.run()

    def isremoved(self):
        """Return a boolean indicating if we must remove stuff."""
        return self.params.get('state') == 'absent'

    def run(self):
        raise NotImplementedError

    def exit(self, *args, **kwargs):
        return self.module.exit_json(changed=self.changed, *args, **kwargs)

    def fail(self, msg, *args, **kwargs):
        return self.module.fail_json(msg=msg, *args, **kwargs)
