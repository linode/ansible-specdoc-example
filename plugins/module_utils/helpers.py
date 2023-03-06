"""
Various helper functions.
"""

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib


def handle_import_error(package_name: str, exc: ImportError):
    """
    Gracefully handles import errors for user-installed packages.
    """
    if __name__ == "__main__":
        AnsibleModule({}).fail_json(
            msg=missing_required_lib(package_name),
            exception=traceback.format_exc(),
        )
