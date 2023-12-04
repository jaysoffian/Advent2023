export PIP_DISABLE_PIP_VERSION_CHECK=1

.PHONY: venv
venv: .direnv/setup.done

.direnv/setup.done: requirements.txt
	pip install --upgrade pip
	pip install -r requirements.txt
	touch "$@"

FORCE:

day%: FORCE
	bin/mkday $(@:day%=%)

test%: FORCE
	pytest -v --doctest-modules $(@:test%=day%)/day*.py

.PHONY: test
test:
	pytest -v --doctest-modules day*/day*.py
