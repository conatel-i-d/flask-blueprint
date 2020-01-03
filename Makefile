.PHONY: test run migration

test:
	pytest --disable-warnings --maxfail 1 -v

build-dev:
	docker build -t conatel-i-d/flask-blueprint:dev -f Dockerfile.dev .

dev:
	docker stop flask-blueprint ;\
	docker rm flask-blueprint ;\
	docker run -it -d \
		-p 8080:8080 \
		-v `pwd`:/usr/src/app \
		-e DATABASE_URI="sqlite:///`pwd`/db/dev.db" \
		--name flask-blueprint \
		conatel-i-d/flask-blueprint:dev

run:
	FLASK_APP=./flask_blueprint.py FLASK_DEBUG=True FLASK_ENV=dev flask run

migration:
	alembic upgrade head
