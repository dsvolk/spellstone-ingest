env:
	poetry install --with dev,test --no-root
	poetry run pre-commit install

env-prod:
	poetry install --no-dev --no-root

test:
	poetry run python -m indexer.cli test
