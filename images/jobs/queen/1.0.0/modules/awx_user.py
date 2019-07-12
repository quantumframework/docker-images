import os

from ansible.module_utils.basic import AnsibleModule
from queen.ext.awx.ansible import UserModule


def main():
    module = UserModule()
    module.handle()


if __name__ == '__main__':
    main()

