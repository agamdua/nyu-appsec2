.PHONY: k8s

runserver:
	FLASK_ENV=development flask run --host 0.0.0.0 --port 8080

prod:
	flask run --host 0.0.0.0 --port 8080

install:
	pip3 install -r requirements.txt

dev_install: install
	pip3 install -r dev_requirements.txt

format:
	black .
	black tests/

test:
	rm -f test.db
	SPELL_CHECK_ENV=CI pytest -s
	rm test.db

build:
	docker build . -t spell-checker

k8s:
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml


ksecrets:
	# this is obviously not a production thing
	# it is for an assignment
	kubectl create secret generic admin --from-file=k8s/secrets/admin_pw --from-file=k8s/secrets/admin_two_factor
