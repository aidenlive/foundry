# Foundry developer workflow. `make setup` once, then `make validate`.
.RECIPEPREFIX := >
.DEFAULT_GOAL := help

VENV := .venv/bin

.PHONY: help setup lint test validate fmt hcl-check docs docs-serve clean

help:
> @echo "setup       create .venv and install the CLI (dev extras)"
> @echo "lint        ruff + yamllint"
> @echo "test        pytest"
> @echo "hcl-check   parse every .tf file"
> @echo "validate    lint + test + foundry validate + hcl-check + docs"
> @echo "fmt         ruff --fix and tofu fmt (when installed)"
> @echo "docs        build the docs site (strict)"
> @echo "docs-serve  live-reload docs server"
> @echo "clean       remove build artifacts"

setup:
> python3 -m venv .venv
> $(VENV)/pip install --quiet --upgrade pip
> $(VENV)/pip install --quiet -e "./cli[dev]"
> @echo "done — activate with: source .venv/bin/activate"

lint:
> $(VENV)/ruff check cli
> $(VENV)/yamllint -c .yamllint.yml .

test:
> $(VENV)/python -m pytest cli/tests -q

hcl-check:
> $(VENV)/python scripts/check_hcl.py .

validate: lint test hcl-check
> $(VENV)/foundry validate
> $(VENV)/mkdocs build --strict --quiet
> @echo "all checks passed"

fmt:
> $(VENV)/ruff check --fix cli
> command -v tofu >/dev/null && tofu fmt -recursive modules stacks || true

docs:
> $(VENV)/mkdocs build --strict

docs-serve:
> $(VENV)/mkdocs serve

clean:
> rm -rf site cli/dist cli/build cli/*.egg-info
> find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} +
