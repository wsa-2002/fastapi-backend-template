default: help

.PHONY: help test coverage run dev docker-build docker-build-x86 docker-run docker-stop docker-rm redis

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

test: # run unit test for backend service
	poetry run isort .
	poetry run pycodestyle --ignore "E501, E402, W503, W504" app
	poetry run coverage run --source=app -m unittest -v
	poetry run coverage report

install: # install dependencies
	poetry install
	pre-commit install
	cp .env.example .env

coverage: # show coverage report
	poetry run coverage report

run: # run service without reload flag
	poetry run uvicorn app.main:app

dev: # run service with reload flag
	poetry run uvicorn app.main:app --reload

build: # build docker image
	docker build -t backend .

build-x86: # build x86_64 docker image
	docker build --platform=linux/amd64 -t backend .

docker-run: # run docker container with newest image of "backend", backend port would be 8000
	docker run -d --name backend -p 8000:80 backend

docker-stop: # stop backend container
	docker stop backend

docker-rm: # rm backend container
	docker rm backend

redis: # run redis docker
	docker run -d --rm --name redis -p 6379:6379 redis

helm: # helm upgrade
	helm upgrade backend deploy/helm/charts \
        --install \
        --namespace=default  \
        --values deploy/helm/production/values.yaml \
        --set image.tag=latest

show-url: # show helm deployment's service url
	NODE_PORT=$(shell kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services backend); \
	NODE_IP=$(shell kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}"); \
	echo http://$${NODE_IP}:$${NODE_PORT}
