PYTHON=./.venv/bin/python

.PHONY: run test locust migrate clean createsuperuser collectstatic


run: 
	@$(PYTHON) manage.py runserver

test:
	@$(PYTHON) manage.py test --settings=django_project.settings.test

locust:
	@echo "(info) Needs to call this command first -> $ make run"
	locust --host=http://127.0.0.1:8000


_makemigration:
	$(PYTHON) manage.py makemigrations


migrate: _makemigration
	 $(PYTHON) manage.py migrate

# TODO; needs to fix ModuleNotFoundError: No module named 'django.db.migrations.migration'
# to fix just command below after make clean
# $ poetry remove django && poetry add django@^4.2.1
clean:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	find . -path "*/__pycache__/*" -delete
	rm -f db.sqlite3
	rm -rf static/
	@echo "Cleaned up."

createsuperuser:
	@$(PYTHON) manage.py createsuperuser

collectstatic:
	@$(PYTHON) manage.py collectstatic --noinput


