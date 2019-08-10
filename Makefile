.PHONY: test run

test:
	pytest --disable-warnings

run:
	FLASK_APP=./flask_blueprint.py FLASK_DEBUG=True FLASK_ENV=dev flask run