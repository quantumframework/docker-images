
import os

from ansible.module_utils.basic import AnsibleModule
from queen.ext.awx.ansible import JobTemplateCredentialModule


def main():
    module = JobTemplateCredentialModule()
    module.handle()


if __name__ == '__main__':
    main()
