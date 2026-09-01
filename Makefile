# ==============================================================================
# MaintAI DevOps Makefile
# Automation targets for development, containerization, and operations
# ==============================================================================

.PHONY: help install dev build lint typecheck docker-build docker-run docker-up docker-down docker-logs health clean k8s-apply

help: ## Show available commands
	@echo "MaintAI DevOps Command Center"
	@echo "----------------------------------------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- Local Development ---
install: ## Install application dependencies
	npm ci

dev: ## Run Next.js local development server
	npm run dev

build: ## Build Next.js production standalone bundle
	npm run build

lint: ## Run ESLint checks
	npm run lint

typecheck: ## Run TypeScript type-checker without emitting files
	npm run typecheck

# --- Docker Operations ---
docker-build: ## Build optimized production Docker image
	docker build -t maintai:latest .

docker-run: ## Run Docker container locally on port 3000
	docker run --rm -p 3000:3000 --env-file .env.local --name maintai-test maintai:latest

docker-up: ## Start production stack in background via Docker Compose
	docker compose up -d

docker-up-proxy: ## Start production stack with Nginx reverse proxy
	docker compose --profile proxy up -d

docker-down: ## Stop Docker Compose stack
	docker compose down

docker-dev: ## Run containerized development environment with hot reload
	docker compose -f docker-compose.dev.yml up

docker-logs: ## View container logs in real time
	docker compose logs -f maintai-app

# --- Health & Observability ---
health: ## Query local health check endpoint
	@curl -s -i http://localhost:3000/api/health || echo "Unable to connect to http://localhost:3000/api/health"

# --- Kubernetes ---
k8s-apply: ## Apply Kubernetes manifests to the active cluster
	kubectl apply -f deploy/k8s/configmap.yaml
	kubectl apply -f deploy/k8s/deployment.yaml
	kubectl apply -f deploy/k8s/service.yaml
	kubectl apply -f deploy/k8s/ingress.yaml
	kubectl apply -f deploy/k8s/hpa.yaml

clean: ## Remove build artifacts, caches, and temporary files
	rm -rf .next
	rm -rf out
	rm -rf node_modules/.cache
