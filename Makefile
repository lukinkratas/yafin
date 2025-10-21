.PHONY: install install-all install-dev install-test format format lint lint-fix typecheck test test-int test-all build doc

help:
	@echo "Available targets:"
	@echo "  install        - Install the package and its dependencies"
	@echo "  install-all    - Install the package with all extras"
	@echo "  install-dev    - Install the package with dev dependencies"
	@echo "  install-test   - Install the package with test dependencies"
	@echo "  format         - Format the code using ruff"
	@echo "  lint           - Check linting of the code using ruff"
	@echo "  lint-fix       - Check and fix linting of the code using ruff"
	@echo "  typecheck      - Type check the code using mypy"
	@echo "  test           - Run unit tests"
	@echo "  test-int       - Run integration tests"
	@echo "  test-all       - Run all tests with html coverage"
	@echo "  clean          - Removes htmlcov, __pycache__, pytest mypy and ruff cache dirs"
	@echo "  build          - Build package - bdist wheel and sdist"
	@echo "  doc            - build documentation html"
	@echo "  help           - Show this help message"

install:
	uv sync

install-all:
	uv sync --all-extras

install-dev:
	uv sync --extra dev

install-test:
	uv sync --extra test

format:
	uv run --group dev ruff format

lint:
	uv run --group dev ruff check

lint-fix:
	uv run --group dev ruff check --fix

typecheck:
	uv run --group dev mypy .

test:
	uv pip install -e .
	uv run --group test pytest -m "not integration and not performance and not baseline" -p no:warnings --cov=yafin --cov-report=term-missing --cov-branch

test-int:
	uv pip install -e .
	uv run --group test pytest -m integration -p no:warnings --cov=yafin --cov-report=term-missing --cov-branch

test-all:
	uv pip install -e .
	uv run --group test pytest --cov=yafin --cov-report=term-missing --cov-branch --cov-fail-under=95 --cov-report=html:htmlcov

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache htmlcov .ruff_cache .coverage main.log dist *.egg-info

build:
	uv build

doc:
	uv run --group doc mkdocs build
	uv run --group doc mkdocs serve