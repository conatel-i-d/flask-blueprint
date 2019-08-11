.PHONY: test run migration

test:
	pytest --disable-warnings --maxfail 1

run:
	FLASK_APP=./flask_blueprint.py FLASK_DEBUG=True FLASK_ENV=dev flask run

migration:
	alembic upgrade head