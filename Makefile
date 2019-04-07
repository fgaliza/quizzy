migrate:
	python quizzy/manage.py migrate

migrations:
	python quizzy/manage.py makemigrations

enable-local:
	@cp local.env .env

lint:
	pipenv run pre-commit run -a -v

test:
	pipenv run pytest -x -s quizzy

runserver:
	python quizzy/manage.py runserver