"""
Generates an ignore file for sanity tests.
This is necessary because the default sanity tests do not
pass with ansible-specdoc as a requirement.
"""

import glob

from packaging import version

from ansible.release import __version__ as ansible_version
from ansible_test._internal.constants import SUPPORTED_PYTHON_VERSIONS

PYTHON_VERSIONS = ["3.11", "3.12", "3.13", "3.14", "3.15"]

parsed_version = version.parse(ansible_version)

with open(f"tests/sanity/ignore-{parsed_version.major}.{parsed_version.minor}.txt", "w") as file:
    file.write("scripts/inject_docs.sh shebang\n")
    file.write("scripts/clear_docs.sh shebang\n")
    file.write("scripts/generate_sanity_ignores.py shebang\n")

    for plugin_file in glob.glob("plugins/**/*.py", recursive=True):
        for ver in PYTHON_VERSIONS:
            if ver in SUPPORTED_PYTHON_VERSIONS:
                file.write(f"{plugin_file} import-{ver}!skip\n")

    for plugin_file in glob.glob("plugins/modules/*.py", recursive=True):
        file.write(f"{plugin_file} validate-modules!skip\n")
