runserver:
	FLASK_ENV=development flask run

install:
	pip install -r requirements.txt

format:
	black .


test:
	rm -f test.db
	pytest -s
	rm test.db
