.PHONY: help build up down restart logs clean ps shell-backend shell-frontend

# Default target - show help
help: ## Show this help message
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker compose build

up: ## Start services in detached mode
	docker compose up -d

down: ## Stop and remove containers
	docker compose down

restart: ## Restart all services
	docker compose restart

logs: ## View logs from all services
	docker compose logs -f

logs-backend: ## View logs from backend only
	docker compose logs -f backend

logs-frontend: ## View logs from frontend only
	docker compose logs -f frontend

ps: ## List running containers
	docker compose ps

shell-backend: ## Open shell in backend container
	docker compose exec backend sh

shell-frontend: ## Open shell in frontend container
	docker compose exec frontend sh

clean: ## Stop containers and remove volumes
	docker compose down -v

clean-all: ## Remove containers, volumes, and images
	docker compose down -v --rmi all

rebuild: down build up ## Rebuild and restart services
