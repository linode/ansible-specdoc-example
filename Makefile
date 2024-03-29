SHELL := /bin/bash
COLLECTIONS_PATH ?= ~/.ansible/collections

TEST_ARGS := -v
INTEGRATION_CONFIG := ./tests/integration/integration_config.yml

clean:
	rm -f *.tar.gz

build: clean
	# Generate and inject the documentation
	./scripts/inject_docs.sh

	# Build the collection
	-ansible-galaxy collection build

	# Remove the generated docs
	./scripts/clear_docs.sh

publish: build
	@if test "$(GALAXY_TOKEN)" = ""; then \
	  echo "GALAXY_TOKEN must be set"; \
	  exit 1; \
	fi
	ansible-galaxy collection publish --token $(GALAXY_TOKEN) *.tar.gz

install: build
	ansible-galaxy collection install *.tar.gz --force -p $(COLLECTIONS_PATH)

deps:
	pip install -r requirements-dev.txt

sanity:
	python3 ./scripts/generate_sanity_ignores.py

	# Generate and inject the documentation
	./scripts/inject_docs.sh

	# Run sanity tests
	-ansible-test sanity

	# Remove the generated docs
	./scripts/clear_docs.sh

lint:
	pylint plugins

	isort --check-only plugins
	autoflake --check plugins --quiet
	black --check plugins

testint:
	ansible-test integration $(TEST_ARGS)

doc-preview: install
	ansible-doc -t module $(DOC_MODULE_NAME)

black:
	black plugins

isort:
	isort plugins

autoflake:
	autoflake plugins

format: black isort autoflake
