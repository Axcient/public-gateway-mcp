@_:
    just --list

# Run linters
[group('qa')]
lint:
    uvx ruff check
    uvx ruff format --check

# Check types
[group('qa')]
typing:
    uv run mypy src

# Run automated fixes
[group('qa')]
fix:
    uvx ruff check --fix
    uvx ruff format

# Perform all checks
[group('qa')]
check-all: lint typing

# Update dependencies
[group('lifecycle')]
update:
    uv sync --upgrade

# Initialize project for local development
[group('lifecycle')]
_bootstrap:
    pre-commit install
    touch .env

# Ensure project virtualenv is up to date
[group('lifecycle')]
install:
    @if ! {{ path_exists(".env") }}; then just _bootstrap; fi
    uv sync

# Remove temporary files
[group('lifecycle')]
clean:
    rm -rf .venv .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
    find . -type d -name "__pycache__" -exec rm -r {} +

# Recreate project virtualenv from nothing
[group('lifecycle')]
fresh: clean install

# Release project
[group('lifecycle')]
release bump:
    uv version --bump {{bump}}
    git add pyproject.toml uv.lock
    git commit -m "🔖 $(uv version --short)"
    git tag v$(uv version --short)
    git push --tags
    uv build
    uv publish
