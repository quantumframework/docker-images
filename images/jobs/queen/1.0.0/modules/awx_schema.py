
import os

from ansible.module_utils.basic import AnsibleModule
from queen.ext.awx.ansible import SchemaModule


def main():
    module = SchemaModule()
    module.handle()


if __name__ == '__main__':
    main()
