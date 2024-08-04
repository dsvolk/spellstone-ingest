env:
	poetry install --with dev,test --no-root
	poetry run pre-commit install

env-prod:
	poetry install --no-dev --no-root

test:
	poetry run python -m indexer.cli test

prefect:
	poetry run prefect server start

## Lint and test
pretty:
	poetry run pre-commit run --all-files

p: pretty

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
