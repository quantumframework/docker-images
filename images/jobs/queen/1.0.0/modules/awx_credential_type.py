import os

from ansible.module_utils.basic import AnsibleModule
from queen.ext.awx.ansible import CredentialTypeModule


def main():
    module = CredentialTypeModule()
    module.handle()


if __name__ == '__main__':
    main()

