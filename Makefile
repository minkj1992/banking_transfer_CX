PYTHON=./.venv/bin/python

.PHONY: run
run: 
	@$(PYTHON) manage.py runserver
