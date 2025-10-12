.PHONY: help build up down restart logs clean test lint format shell health

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)LLM Bootcamp Project - Infrastructure Management$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build

up: build ## Build and start the application
	@echo "$(GREEN)Starting application...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Application is running at http://localhost:8502$(NC)"

up-mcp: ## Start application with MCP server
	@echo "$(GREEN)Starting application with MCP server...$(NC)"
	docker-compose --profile mcp up -d
	@echo "$(GREEN)Application: http://localhost:8502$(NC)"
	@echo "$(GREEN)MCP Server: http://localhost:8000$(NC)"

down: ## Stop the application
	@echo "$(RED)Stopping application...$(NC)"
	docker-compose down

restart: down up ## Restart the application

logs: ## Show application logs
	docker-compose logs -f

logs-app: ## Show only app logs
	docker-compose logs -f streamlit-app

logs-mcp: ## Show only MCP server logs
	docker-compose logs -f mcp-server

shell: ## Open shell in the app container
	docker-compose exec streamlit-app /bin/bash

health: ## Check application health (Docker runtime)
	@echo "$(BLUE)Checking application health...$(NC)"
	@curl -f http://localhost:8502/_stcore/health || echo "$(RED)Application is not healthy$(NC)"

health-check: ## Run comprehensive health check script
	@echo "$(BLUE)Running comprehensive health check...$(NC)"
	@python tests/health_check.py

clean: ## Remove containers, volumes, and images
	@echo "$(RED)Cleaning up Docker resources...$(NC)"
	docker-compose down -v --rmi local
	rm -rf tmp/vectorstores/*

clean-cache: ## Clear vectorstore cache
	@echo "$(YELLOW)Clearing vectorstore cache...$(NC)"
	rm -rf tmp/vectorstores/*

dev: ## Start in development mode with live reload
	@echo "$(GREEN)Starting in development mode...$(NC)"
	docker-compose up

rebuild: ## Rebuild and restart the application
	@echo "$(BLUE)Rebuilding application...$(NC)"
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "$(GREEN)Application rebuilt and running at http://localhost:8502$(NC)"

ps: ## Show running containers
	docker-compose ps

stats: ## Show container resource usage
	docker stats --no-stream

lint: ## Run ruff linting
	@echo "$(BLUE)Running ruff linting...$(NC)"
	@command -v ruff >/dev/null 2>&1 || { echo "$(RED)ruff not installed. Install with: pip install ruff$(NC)"; exit 1; }
	ruff check .

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code with ruff...$(NC)"
	@command -v ruff >/dev/null 2>&1 || { echo "$(RED)ruff not installed. Install with: pip install ruff$(NC)"; exit 1; }
	ruff format .

test: health-check ## Run all tests (health check first)
	@echo "$(BLUE)Running tests...$(NC)"
	docker-compose exec streamlit-app uv run pytest

install-dev: ## Install development dependencies locally
	@echo "$(BLUE)Installing dependencies with uv...$(NC)"
	uv sync

env-template: ## Create .env template file
	@echo "$(BLUE)Creating .env template...$(NC)"
	@echo "# OpenAI API Key\nOPENAI_API_KEY=sk-proj-..." > .env.template
	@echo "# Tavily API Key\nTAVILY_API_KEY=tvly-..." >> .env.template
	@echo "# MCP Server URL\nMCP_SERVER_URL=http://mcp-server:8000" >> .env.template
	@echo "$(GREEN).env.template created. Copy to .env and add your keys.$(NC)"

backup-cache: ## Backup vectorstore cache
	@echo "$(BLUE)Backing up cache...$(NC)"
	tar -czf cache-backup-$$(date +%Y%m%d-%H%M%S).tar.gz tmp/vectorstores/
	@echo "$(GREEN)Cache backed up successfully$(NC)"

prune: ## Remove all unused Docker resources
	@echo "$(RED)Pruning Docker resources...$(NC)"
	docker system prune -af --volumes

.DEFAULT_GOAL := help
