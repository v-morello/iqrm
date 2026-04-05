.DEFAULT_GOAL := help
PKG = iqrm
PKG_DIR = src/
TESTS_DIR = tests/

format: ## Format code using ruff
	ruff check ${PKG_DIR} ${TESTS_DIR} --fix

lint: ## Lint code using ruff
	ruff check ${PKG_DIR} ${TESTS_DIR}

dist: ## Build source distribution
	python setup.py sdist

ci: lint tests ## Run all CI checks

# NOTE: -e installs in "Development Mode"
# See: https://packaging.python.org/tutorials/installing-packages/
install: ## Install the package in development mode
	pip install -e .[dev]

uninstall: ## Uninstall the package
	pip uninstall ${PKG}

# GLORIOUS hack to autogenerate Makefile help
# This simply parses the double hashtags that follow each Makefile command
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Print this help message
	@echo "Makefile help for ${PKG}"
	@echo "===================================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

tests: ## Run unit tests
	pytest --cov=${PKG_DIR} --verbose --cov-report term-missing ${TESTS_DIR}

.PHONY: dist install uninstall help tests ci format lint
