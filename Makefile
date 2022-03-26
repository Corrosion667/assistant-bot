install:
	poetry install --no-root

full-install:
	pip3 install --user poetry==1.2.0b1
	poetry install --no-root

lint:
	poetry run flake8 bots