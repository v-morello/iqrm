.DEFAULT_GOAL := help
PKG = iqrm
TESTS_DIR = ${PKG}/tests

dist: ## Build source distribution
	python setup.py sdist

# NOTE: -e installs in "Development Mode"
# See: https://packaging.python.org/tutorials/installing-packages/
install: ## Install the package in development mode
	pip install -e .

uninstall: ## Uninstall the package
	pip uninstall ${PKG}

# GLORIOUS hack to autogenerate Makefile help
# This simply parses the double hashtags that follow each Makefile command
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Print this help message
	@echo "Makefile help for ${PKG}"
	@echo "===================================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean: ## Remove all python cache and build files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/
	rm -rf dist/
	rm -f .coverage
	rm -rf .pytest_cache

tests: ## Run unit tests
	pytest --cov --verbose --cov-report term-missing ${PKG}/tests

.PHONY: dist install uninstall help clean tests
