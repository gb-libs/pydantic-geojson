.PHONY: help lint ruff-fix clean test


help: ## Display this help screen
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

lint: ## Auto fix lint
	pre-commit run --all-files

ruff-fix: ## Auto fix lint ruff
	ruff check . --fix

clean: ## Clear temp files
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf dist *.egg-info
	rm -rf .cache
	rm -rf .pytest_cache
	rm -f .coverage
	rm -f .coverage.*

test: ## Run tests
	pytest --cov=pydantic_geojson --cov-report=xml
