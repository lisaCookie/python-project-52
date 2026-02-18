build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

run:
	uv run python manage.py runserver

lint:
	ruff check .

lint-fix:
	uv run ruff check --fix

test:
	uv run python manage.py test

migrate:
	uv run python manage.py migrate
