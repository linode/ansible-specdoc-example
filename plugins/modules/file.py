"""
This file contains an implementation of a sample `file` module.
"""

# Required by Ansible
from __future__ import absolute_import, division, print_function

__metaclass__ = type

# These will be populated at build-time
DOCUMENTATION = """"""

RETURN = """"""

EXAMPLES = """"""

import os
from typing import List

from ansible_collections.linode.specdoc_example.plugins.module_utils.base_module import (
    BaseModule,
)
from ansible_collections.linode.specdoc_example.plugins.module_utils.documentation.file import (
    FILE_SAMPLES,
    SPEC_EXAMPLES,
)
from ansible_collections.linode.specdoc_example.plugins.module_utils.helpers import (
    handle_import_error,
)

# User-installed packages must be handled gracefully
try:
    from ansible_specdoc.objects import (
        FieldType,
        SpecDocMeta,
        SpecField,
        SpecReturnValue,
    )
except ImportError as exc:
    handle_import_error("ansible-specdoc", exc)

SPEC = {
    "state": SpecField(
        type=FieldType.string,
        description="The state of the file.",
        required=True,
        choices=["present", "absent"],
    ),
    "path": SpecField(
        type=FieldType.string,
        description="The path of the file.",
        required=True,
    ),
    "create_directories": SpecField(
        type=FieldType.bool,
        default=True,
        description="Whether or not to create parent directories if they do not exist.",
    ),
    "permissions": SpecField(
        type=FieldType.string,
        description="The permissions to give the file.",
        default="644",
    ),
    "content": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description="A list of lines to write to the file.",
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Create, update, and destroy files.",
    ],
    requirements=["Python >= 3.9"],
    author=["Lena Garber (@lgarber-akamai)"],
    options=SPEC,
    examples=SPEC_EXAMPLES,
    return_values=dict(
        file=SpecReturnValue(
            description="Info about the resulting file.",
            type=FieldType.dict,
            sample=FILE_SAMPLES,
        ),
    ),
)


class Module(BaseModule):
    """
    An example module class.
    """

    _file_path = None

    def _get_input_lines(self) -> List[str]:
        """
        Gets the content from the `content` field.
        """

        content = self.module.params.get("content")

        return [f"{v}\n" for v in content or []]

    def _write_file(self):
        """
        Writes the content defined in the `content` field to the file.
        """

        with open(self._file_path, "w", encoding="utf-8") as file:
            file.writelines(self._get_input_lines())

    def _read_file(self) -> List[str]:
        """
        Reads the file.
        """
        with open(self._file_path, "r", encoding="utf-8") as file:
            return file.readlines()

    def _delete_file(self):
        """
        Deletes the file.
        """

        os.remove(self._file_path)

    def _attempt_update_file_content(self):
        """
        Attempts to update the file's content if there is a mismatch.
        """

        if self._read_file() == self._get_input_lines():
            return

        self.register_action(f"Updated file content for {self._file_path}")
        self._write_file()

    def _attempt_update_permissions(self):
        """
        Attempts to update the file's permissions if there is a mismatch.
        """

        desired_permission_mask = int(self.module.params.get("permissions"), 8)

        stat = os.stat(self._file_path)
        actual_permission_mask = stat.st_mode & 0o777

        if actual_permission_mask == desired_permission_mask:
            return

        self.register_action(
            f"Updated file permissions "
            f"{oct(actual_permission_mask)[2:]} -> {oct(desired_permission_mask)[2:]}"
        )

        os.chmod(self._file_path, desired_permission_mask)

    def _attempt_create_parent_directories(self):
        """
        Attempts to create the parent directories of the file if they do not exist.
        Returns early if create_directories is False.
        """

        path = os.path.dirname(self._file_path)
        if not self.module.params.get("create_directories"):
            return

        if os.path.isdir(path):
            return

        self.register_action(f"Created path {path}")
        os.makedirs(path, exist_ok=True)

    def _populate_results(self):
        """
        Populates the module results.
        """

        file_info = os.stat(self._file_path)

        self.result["file"] = {
            "size": file_info.st_size,
            "permissions": oct(file_info.st_mode & 0o777)[2:],
            "path": self._file_path,
        }

    def _handle_present(self):
        """
        Executes on status `present`
        """

        # Attempt to recursively create parent directories
        self._attempt_create_parent_directories()

        if not os.path.isfile(self._file_path):
            # Create the file if it doesn't exist
            self._write_file()
            self.register_action(f"Created file {self._file_path}")
        else:
            # Otherwise, attempt to update the file's content
            self._attempt_update_file_content()

        self._attempt_update_permissions()

        self._populate_results()

    def _handle_absent(self):
        """
        Executes on state `absent`.
        """

        if not os.path.isfile(self._file_path):
            return

        self._populate_results()
        self._delete_file()
        self.register_action(f"Deleted file {self._file_path}")

    def handle_call(self):
        """
        The entrypoint of the module.
        """

        self._file_path = self.module.params.get("path")

        {"present": self._handle_present, "absent": self._handle_absent}[
            self.module.params.get("state")
        ]()


if __name__ == "__main__":
    Module(SPECDOC_META).run()
