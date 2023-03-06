"""
Contains a base class for use in modules.
"""

# Required by Ansible
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linode.specdoc_example.plugins.module_utils.helpers import (
    handle_import_error,
)

try:
    from ansible_specdoc.objects import SpecDocMeta
except ImportError as exc:
    handle_import_error("ansible-specdoc", exc)


class BaseModule:
    """
    A base class that handles module actions, returns, etc.
    """

    def __init__(self, spec: SpecDocMeta, **kwargs):
        self.module = AnsibleModule(argument_spec=spec.ansible_spec, **kwargs)

        self.result = {"changed": False, "actions": []}

    def register_action(self, message):
        """
        Registers the given action and sets `changed` to True.
        """

        self.result["actions"].append(message)
        self.result["changed"] = True

    def handle_call(self):
        """
        The entrypoint of the module.
        This function should be implemented in each module.
        """

    def run(self):
        """
        Runs the module.
        """

        try:
            self.handle_call()
        except Exception as err:
            self.module.fail_json(msg=str(err))
            return

        self.module.exit_json(**self.result)
