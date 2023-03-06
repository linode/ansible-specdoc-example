# ansible-specdoc-example

An example Ansible Collection using ansible-specdoc to generate module specification and documentation. 

This project exposes a `file` module that allows users to create and manage simple files through Ansible.

**NOTE: The file module was created exclusively as an example and should not be used in production playbooks.**

## Setup

This section will guide you through the basic setup process for this repository.

### Cloning the Repository

When developing Ansible Collections, users are required to follow a specific directory structure.
Due to how this project renders documentation, it will need to be stored _outside_ of the `~/.ansible` directory.

This can be achieved by running the following command in your desired project directory:

```bash
mkdir -p ansible_collections/linode
```

From here, you can clone this repository:

```bash
git clone git@github.com:linode/ansible-specdoc-example.git ansible_collections/linode/specdoc_example
```

Now you can enter the project directory:

```bash
cd ansible_collections/linode/specdoc_example
```

### Setting Up a Virtual Environment (Optional)

To keep your project dependencies separate from your system dependencies, it is recommended that you set up a [Python virtual environment](https://docs.python.org/3/library/venv.html).

To create the environment in the `venv` directory, run:

```bash
python3 -m venv venv
```

You can then enter this environment by running:

```bash
source venv/bin/activate
```

### Installing the Collection

To install the dependencies for this project, run the following:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

From here you can run the following Makefile target to install the collection:

```bash
make install
```

This collection should now be available to use through playbooks.

Please refer to the [Makefile Targets](#makefile-targets) section for information about running integration and sanity tests, building the project, and previewing documentation.

## Makefile Targets

This project includes a few Makefile targets to allow for easier project testing and vetting.

### Integration Testing

Running the entire integration test suite:

```bash
make testint
```

Running a single integration test:

```bash
make TEST_ARGS="-v file_basic" testint
```

### Sanity Testing

Run sanity tests for the entire project:

```bash
make sanity
```

### Previewing Documentation

Preview documentation for an individual module:

```bash
make DOC_MODULE_NAME=linode.specdoc_example.file doc-preview
```

## Collection structure

- `plugins`: Contains collection modules and helpers
  - `modules`: Contains all the module implementations for this colleciton
    - `file.py`: Logic and spec for the `file` module
  - `module_utils`: Contains shared helpers for use in modules
    - `documentation`: Contains documentation strings for use in modules
      - `file.py`: Documentation fragments for the `file` module
    - `base_module.py`: Base module class to be consumed by modules
    - `helpers.py`: Various shared helper functions
- `scripts`: Contains various helper scripts
  - `generate_sanity_ignores.py`: Generates a sanity test ignore file to disable sanity tests that are incompatible with ansible-specdoc.
  - `inject_docs.sh`: Injects generated documentation strings into each Ansible module
- `tests`: Contains testing configuration and playbook
  - `integration/targets/file_basic/tasks/main.yaml`: The `file_basic` integration test case
  - `sanity`: Contains sanity test ignore files
  - `config.yml`: Used to set the minimum supported Python version for testing

## Contribution Guidelines

Want to improve ansible-specdoc-example? Please start [here](CONTRIBUTING.md).
