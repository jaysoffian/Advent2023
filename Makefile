export PIP_DISABLE_PIP_VERSION_CHECK=1

.direnv/setup.done: requirements.txt
	pip install --upgrade pip
	pip install -r requirements.txt
	touch "$@"

day%: FORCE
	bin/download "$@"

test:
	pytest -v --doctest-modules day*/day*.py

FORCE:
