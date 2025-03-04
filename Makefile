ifneq ($(wildcard .env.example),)
    ENV_FILE = .env.example
endif
ifneq ($(wildcard .env.example),)
	ifeq ($(COMPOSE_PROJECT_NAME),)
    	include .env.example
	endif
endif
ifneq ($(wildcard .env),)
    ENV_FILE = .env
endif
ifneq ($(wildcard .env),)
	ifeq ($(COMPOSE_PROJECT_NAME),)
		include .env
	endif
endif

docker_compose = docker compose -f docker-compose.yml --env-file $(ENV_FILE)
docker_compose_development = docker compose -f docker-compose.development.yml --env-file $(ENV_FILE)

export

.SILENT:
.PHONY: help
help: ## Display this help screen
	awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

.PHONY: install
install: ## Installations
	poetry env use python
	poetry install
	poetry run pre-commit install

.PHONY: test
test: ## Test applications
	poetry run pytest

.PHONY: run-api
run-api: ## Run backend
	poetry run gunicorn --reload --bind $(HOST):$(BACKEND_PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--workers $(API_WORKERS) --log-level $(LEVEL) --chdir cmd/api main:app

.PHONY: develop-api
develop-api: ## Hot reload backend
	poetry run uvicorn src.server:app --reload --host 0.0.0.0 --port 8080 --log-level debug

.PHONY: compose-build
compose-build: ## Build or rebuild services
	$(docker_compose) build

.PHONY: compose-build-develop
compose-build-develop: ## Build or rebuild services
	$(docker_compose_development) build

.PHONY: compose-up
compose-up: ## Create and start containers
	$(docker_compose) up -d

.PHONY: compose-develop
compose-develop: ## Create and start containers in development mode
	$(docker_compose_development) up -d

.PHONY: compose-logs
compose-logs: ## View output from containers
	$(docker_compose) logs -f

.PHONY: compose-ps
compose-ps: ## List containers
	$(docker_compose) ps

.PHONY: compose-ls
compose-ls: ## List running compose projects
	$(docker_compose) ls

.PHONY: compose-exec
compose-exec: ## Execute a command in a running container
	$(docker_compose) exec backend bash

.PHONY: compose-start
compose-start: ## Start services
	$(docker_compose) start

.PHONY: compose-restart
compose-restart: ## Restart services
	$(docker_compose) restart

.PHONY: compose-stop
compose-stop: ## Stop services
	$(docker_compose) stop

.PHONY: compose-down
compose-down: ## Stop and remove containers, networks
	$(docker_compose_development) down --remove-orphans

.PHONY: docker-clean
docker-clean: ## Remove unused data
	docker system prune