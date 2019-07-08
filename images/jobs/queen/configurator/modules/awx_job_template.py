
import os

from ansible.module_utils.basic import AnsibleModule
from queen.ext.awx.ansible import JobTemplateModule


def main():
    module = JobTemplateModule()
    module.handle()


if __name__ == '__main__':
    main()
