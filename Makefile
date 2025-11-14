.PHONY: help install install-dev format pre-commit type-check security test check clean build

help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	poetry install --no-dev

install-dev: ## Install development dependencies
	poetry install

format: ## Format code with ruff and isort
	poetry run ruff format .
	poetry run ruff check --fix .
	poetry run isort .

pre-commit: ## Run pre-commit on all files
	poetry run pre-commit run --all-files

type-check: ## Run type checking with mypy
	poetry run mypy pydantic_geojson

security: ## Run security check with bandit
	poetry run bandit -r pydantic_geojson

test: ## Run tests with coverage
	poetry run pytest

check: pre-commit type-check security test ## Run all checks (pre-commit, type-check, security, test)

clean: ## Remove temporary files and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete
	find . -type f -name '.*~' -delete
	rm -rf dist build *.egg-info .eggs
	rm -rf .cache .pytest_cache .coverage htmlcov
	rm -f .coverage.* coverage.xml
	rm -rf .mypy_cache .ruff_cache

build: ## Build package
	poetry build
