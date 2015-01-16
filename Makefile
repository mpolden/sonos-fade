all: lint

lint:
	find . -name '*.py' | xargs flake8 --max-complexity=8
