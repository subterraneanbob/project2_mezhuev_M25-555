install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run
