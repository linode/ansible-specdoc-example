"""
This module contains documentation strings for use in the `file` module.
"""

__metaclass__ = type

SPEC_EXAMPLES = [
    """
- name: Create a file
  linode.specdoc_example.file:
    path: foo.txt
    content:
      - line1
      - line2
    permissions: 777
    state: present
""",
    """
- name: Delete a file
  linode.specdoc_example.file:
    path: foo.txt
    state: absent
""",
]

FILE_SAMPLES = ["""{"file": {"size": 12, "permissions": "644", "path": "/path/to/my/file"}}"""]
