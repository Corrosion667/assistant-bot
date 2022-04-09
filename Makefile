install:
	poetry install --no-root

full-install:
	pip3 install --user poetry==1.2.0b1
	make install

lint:
	poetry run flake8 bots

run-tg:
	poetry run tg

run-vk:
	poetry run vk

teach-agent:
	poetry run teach-agent