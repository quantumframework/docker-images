import os

from ansible.module_utils.basic import AnsibleModule
from queen.ext.awx.ansible import TeamModule


def main():
    module = TeamModule()
    module.handle()


if __name__ == '__main__':
    main()

