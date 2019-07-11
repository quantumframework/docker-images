import os

from ansible.module_utils.basic import AnsibleModule
from queen.ext.awx.ansible import CredentialModule


def main():
    module = CredentialModule()
    module.handle()


if __name__ == '__main__':
    main()

