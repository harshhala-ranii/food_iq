.PHONY: help lint-backend lint-frontend test-backend test-coverage docker-build docker-up docker-down install-backend install-frontend install-all db-init-food db-init-auth db-init clean format-backend format-frontend check-css db-remove-duplicates db-remove-column run-with-llm download-llm-model

# Node.js version to use
NODE_VERSION ?= 20

# Default target
help:
	@echo "Available commands:"
	@echo "  make help                 - Show this help message"
	@echo "  make lint                 - Run linting on both backend and frontend"
	@echo "  make lint-backend         - Run flake8 linting on backend code"
	@echo "  make lint-frontend        - Run ESLint on frontend code"
	@echo "  make format-backend       - Format backend code with Black"
	@echo "  make format-frontend      - Format frontend code with Prettier"
	@echo "  make format               - Format both backend and frontend code"
	@echo "  make check-css            - Check CSS files for syntax errors"
	@echo "  make test                 - Run all tests"
	@echo "  make test-backend         - Run backend tests"
	@echo "  make test-coverage        - Run backend tests with coverage report"
	@echo "  make install              - Install all dependencies"
	@echo "  make install-backend      - Install backend dependencies"
	@echo "  make install-frontend     - Install frontend dependencies"
	@echo "  make db-init              - Initialize the database"
	@echo "  make db-remove-duplicates - Remove duplicate records from the database"
	@echo "  make db-remove-column     - Remove the average_volume column from the database"
	@echo "  make docker-build         - Build all Docker images"
	@echo "  make docker-up            - Start all services with Docker Compose"
	@echo "  make docker-down          - Stop all services"
	@echo "  make clean                - Remove build artifacts and cache files"
	@echo "  make run-with-llm         - Run the application with LLM integration"
	@echo "  make download-llm-model   - Download the Llama 3 8B Instruct model"
	@echo ""
	@echo "You can specify a different Node.js version with NODE_VERSION:"
	@echo "  make lint-frontend NODE_VERSION=16"

# Linting
lint: lint-backend lint-frontend

lint-backend:
	@echo "Linting backend code..."
	@echo "Ensuring flake8 is installed..."
	pip install flake8 --quiet
	cd backend && flake8 --count --select=E9,F63,F7,F82 --show-source --statistics .
	cd backend && flake8 --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics .

lint-frontend:
	@echo "Linting frontend code..."
	cd frontend && bash -c 'source $$NVM_DIR/nvm.sh && nvm use $(NODE_VERSION) && npm run lint'

# CSS Syntax Check
check-css:
	@echo "Checking CSS files for syntax errors..."
	@echo "Ensuring stylelint is installed..."
	cd frontend && bash -c 'source $$NVM_DIR/nvm.sh && nvm use $(NODE_VERSION) && npm install --no-save stylelint stylelint-config-standard'
	cd frontend && bash -c 'source $$NVM_DIR/nvm.sh && nvm use $(NODE_VERSION) && npx stylelint "src/**/*.css" --fix || (echo "Warning: Some CSS syntax errors could not be automatically fixed." && exit 0)'

# Formatting
format: format-backend format-frontend

format-backend:
	@echo "Formatting backend code with Black..."
	@echo "Checking if Poetry is installed..."
	@if ! command -v poetry &> /dev/null; then \
		echo "Poetry not found. Installing Poetry..."; \
		curl -sSL https://install.python-poetry.org | python3 -; \
	fi
	@echo "Ensuring Black is installed in Poetry environment..."
	cd backend && poetry add --group dev black || true
	cd backend && poetry run black .

format-frontend: check-css
	@echo "Formatting frontend code with Prettier..."
	@echo "Ensuring Prettier is installed..."
	cd frontend && bash -c 'source $$NVM_DIR/nvm.sh && nvm use $(NODE_VERSION) && npm install --no-save prettier'
	@echo "Running Prettier on frontend code..."
	cd frontend && bash -c 'source $$NVM_DIR/nvm.sh && nvm use $(NODE_VERSION) && npx prettier --write "src/**/*.{js,jsx,ts,tsx,json,css,scss,md}" || (echo "Error: Prettier formatting failed. Check for syntax errors in your files." && exit 1)'
	@echo "Frontend code formatting complete."

# Testing
test: test-backend

test-backend:
	@echo "Running backend tests..."
	@echo "Ensuring pytest is installed..."
	pip install pytest --quiet
	cd backend && pytest

test-coverage:
	@echo "Running backend tests with coverage..."
	@echo "Ensuring pytest-cov is installed..."
	pip install pytest pytest-cov --quiet
	cd backend && pytest --cov=. --cov-report=term --cov-report=xml

# Installation
install: install-backend install-frontend

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && bash -c 'source $$NVM_DIR/nvm.sh && nvm use $(NODE_VERSION) && npm ci'

# Database
db-init-food:
	@echo "Initializing food database tables..."
	cd backend && python db/dbcreateandinsert.py

db-init-auth:
	@echo "Initializing auth database tables..."
	cd backend && python db/init_auth.py

db-init: db-init-auth db-init-food
	@echo "Database initialization complete"

# Docker commands
docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting services..."
	docker-compose up -d

docker-down:
	@echo "Stopping services..."
	docker-compose down

# Frontend development server
frontend-dev:
	@echo "Starting frontend development server..."
	cd frontend && bash -c 'source $$NVM_DIR/nvm.sh && nvm use $(NODE_VERSION) && npm run dev'

# Clean up
clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .coverage -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "coverage.xml" -delete

# Database - Remove duplicates
db-remove-duplicates:
	@echo "Removing duplicate records from the database..."
	@echo "Ensuring required packages are installed..."
	pip install sqlalchemy --quiet
	cd backend && python remove_duplicates.py

# Database - Remove column
db-remove-column:
	@echo "Removing average_volume column from the database..."
	@echo "Ensuring required packages are installed..."
	pip install sqlalchemy --quiet
	cd backend && python remove_column.py

# LLM Integration
run-with-llm:
	@echo "Starting Food IQ with LLM integration..."
	docker-compose -f docker-compose.llm.yml up

download-llm-model:
	@echo "Creating llm-models directory if it doesn't exist..."
	mkdir -p llm-models
	@echo "Downloading Llama 3 8B Instruct model (Q4_K_M quantization)..."
	curl -L https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF/resolve/main/llama-3-8b-instruct.Q4_K_M.gguf -o llm-models/llama-3-8b-instruct.Q4_K_M.gguf
	@echo "Model downloaded successfully to llm-models directory." 