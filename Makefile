.PHONY: k8s

runserver:
	FLASK_ENV=development flask run --host 0.0.0.0

prod:
	flask run --host 0.0.0.0

install:
	pip3 install -r requirements.txt

dev_install: install
	pip3 install -r dev_requirements.txt

format:
	black .
	black tests/

test:
	rm -f test.db
	pytest -s
	rm test.db

build:
	docker build . -t spell-checker

k8s:
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
