.PHONY: install install-all install-dev install-test install-doc install-editable format format lint lint-fix typecheck fetch-mocks test test-int test-perf test-build test-all doc doc-serve build publish changelog

help:
	@echo "Available targets:"
	@echo "  install          - Install the package and its dependencies"
	@echo "  install-all      - Install the package with all extras"
	@echo "  install-dev      - Install the package with dev dependencies"
	@echo "  install-test     - Install the package with test dependencies"
	@echo "  install-doc      - Install the package with doc dependencies"
	@echo "  install-editable - Make the package installation editable"
	@echo "  format           - Format the code using ruff"
	@echo "  lint             - Check linting of the code using ruff"
	@echo "  lint-fix         - Check and fix linting of the code using ruff"
	@echo "  typecheck        - Type check the code using mypy"
	@echo "  fetch-mocks      - Run script to fetch json mocks for fixtures"
	@echo "  test             - Run unit tests"
	@echo "  test-int         - Run integration tests"
	@echo "  test-perf        - Run performance tests"
	@echo "  test-build       - Test built package"
	@echo "  test-all         - Run all tests with html coverage"
	@echo "  clean            - Clean up - remove htmlcov, __pycache__, pytest mypy and ruff cache dirs"
	@echo "  doc              - build documentation html"
	@echo "  doc-serve        - serve documentation html"
	@echo "  build            - Build package - bdist wheel and sdist"
	@echo "  publish          - Publish the package to pypi.org"
	@echo "  changelog        - Create CHANGELOG.md from git log"
	@echo "  help             - Show this help message"

install:
	uv sync

install-all:
	uv sync --all-extras

install-dev:
	uv sync --group dev

install-test:
	uv sync --group test

install-doc:
	uv sync --group doc

install-editable:
	uv pip install -e .

format:
	uv run --group dev ruff format

lint:
	uv run --group dev ruff check

lint-fix:
	uv run --group dev ruff check --fix

typecheck:
	uv run --group dev mypy .

fetch-mocks:
	uv run --group dev python -m scripts.fetch_mocks

test:
	$(MAKE) install-editable
	uv run --group test pytest tests/unit -p no:warnings --cov=yafin --cov-report=term-missing --cov-branch

test-int:
	$(MAKE) install-editable
	uv run --group test pytest tests/integration -p no:warnings

test-perf:
	$(MAKE) install-editable
	uv run --group test pytest tests/performance --benchmark-autosave -p no:warnings

test-build:
	uv run --isolated --no-project --with dist/*.whl pytest tests/unit
	uv run --isolated --no-project --with dist/*.tar.gz pytest tests/unit

test-all:
	$(MAKE) install-editable
	uv run --group test pytest tests/ -m "not performance" --cov=yafin --cov-report=term-missing --cov-branch --cov-fail-under=95 --cov-report=html:htmlcov

clean:
	rm -rvf __pycache__ scripts/__pycache__ tests/__pycache__ tests/integration/__pycache__ tests/unit/__pycache__ yafin/__pycache__ .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov main.log dist yafin.egg-info site *.csv

doc:
	$(MAKE) install-editable
	uv run --group doc mkdocs build

doc-serve:
	uv run --group doc mkdocs serve

build:
	uv build

publish:
	[[ -n $UV_PUBLISH_TOKEN ]] && uv publish || echo "Env var UV_PUBLISH_TOKEN not set."

changelog:
	git log \
		--decorate-refs-exclude=HEAD \
		--decorate-refs-exclude="refs/remotes/*" \
		--decorate-refs-exclude="refs/heads/*" \
		--pretty=format:"%(decorate:prefix=%n,suffix=%n,separator=|,tag=##,pointer=) - %s" > CHANGELOG.md
