# variables
PYVER  := 3.11
venv   := .venv
python := $(venv)/bin/python
pip    := $(venv)/bin/pip


##@ Utility
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z\._-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


##@ Setup
$(venv):
	python$(PYVER) -m venv $(venv);

##@ Development
.PHONY: dev
dev: $(venv) ## install dev mode
	$(pip) install -e .

.PHONY: test
test: $(venv) ## run tests
	@$(pip) -q install pytest
	$(python) -m pytest tests

.PHONY: lint
lint: $(venv)  ## run linting check
	@$(pip) -q install ruff
	$(python) -m ruff ./src

.PHONY: black
black: $(venv)  ## apply black to source code
	@$(pip) -q install black
	$(python) -m black -l79


.PHONY: requirements.txt
requirements.txt:  ## generate requirements.txt, e.g. make requirements.txt
	@test -d /tmp/venv && rm -r /tmp/venv || true
	@$(python) -m venv /tmp/venv
	@/tmp/venv/bin/python -m pip -q install pip -U
	@/tmp/venv/bin/python -m pip -q install . --progress-bar off
	@/tmp/venv/bin/python -m pip freeze > requirements.txt
	$(MAKE) fix-requirements.txt

.PHONY: fix-requirements.txt
fix-requirements.txt:  ## fix requirements.txt using GH_TOKEN variable for privates repos.
	@if [ "$(shell uname -s)" = "Linux" ]; then \
		sed -i 's/git+ssh:\/\/git@/git+https:\/\/$${GH_TOKEN}@/' requirements.txt; \
		sed -i '/file:/d' requirements.txt; \
	elif [ "$(shell uname -s)" = "Darwin" ]; then \
		sed -i '' -e 's/git+ssh:\/\/git@/git+https:\/\/$${GH_TOKEN}@/' requirements.txt; \
		sed -i '' -e '/file:/d' requirements.txt; \
	fi
	@cat requirements.txt
