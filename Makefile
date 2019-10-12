runserver:
	FLASK_ENV=development flask run

install_test:
	pip install -r requirements_test.txt

test:
	pytest
