.PHONY: help test install_all_dependencies install_dependencies install_dev_dependencies setup_environment

POETRY_VERSION := 1.8.4

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

cicd_test: install_all_dependencies test

test:
	ruff check --force-exclude . -v
	ruff format --force-exclude --check . -v
	pytest -m "unit_test or integration_test" .

install_all_dependencies: install_dependencies install_dev_dependencies

install_dependencies: setup_environment
	poetry install --no-interaction --no-ansi

install_dev_dependencies: setup_environment
	poetry install --with dev --no-interaction --no-ansi

setup_environment:
	pip install --no-cache-dir --upgrade pip
	pip install poetry==$(POETRY_VERSION)
	poetry config virtualenvs.create false
