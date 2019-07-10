import os

from ansible.module_utils.basic import AnsibleModule
from queen.ext.awx import InventoryGroupModule


def main():
    module = InventoryGroupModule()
    module.handle()


if __name__ == '__main__':
    main()
