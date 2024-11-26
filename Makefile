.PHONY: test
activate := . .venv/bin/activate

test: | .venv/
	$(activate) && python3 -m doctest -vv *py


.venv/: requirements.txt
	test -d .venv || python3 -m venv .venv/
	$(activate) && python3 -m pip install -r requirements.txt
	touch .venv/
