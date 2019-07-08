
import os

from ansible.module_utils.basic import AnsibleModule
from queen.ext.awx.ansible import InventoryHostModule


def main():
    module = InventoryHostModule()
    module.handle()


if __name__ == '__main__':
    main()
