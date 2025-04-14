# Food IQ Application

A web application for retrieving nutritional information about food items and identifying Indian food from images.

## Table of Contents
1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Setup](#setup)
   - [Environment Configuration](#environment-configuration)
   - [Database Setup](#database-setup)
   - [Model Setup](#model-setup)
5. [Development](#development)
   - [Using Makefile](#using-makefile)
   - [Backend Development](#backend-development)
   - [Frontend Development](#frontend-development)
   - [Database Management](#database-management)
6. [Deployment](#deployment)
   - [Docker Deployment](#docker-deployment)
   - [Local Deployment](#local-deployment)
7. [API Documentation](#api-documentation)
   - [Food Endpoints](#food-endpoints)
   - [Image Processing Endpoints](#image-processing-endpoints)
8. [Testing](#testing)
9. [CI/CD Pipeline](#cicd-pipeline)

## Features

- **Food Nutritional Information**: Get detailed nutritional information about various food items
- **Food Image Recognition**: Upload an image of Indian food and get it identified using our trained CNN model
- **Nutritional Information**: Get detailed nutritional facts for the identified food
- **Manual Search**: Search for foods by name if you already know what you're eating
- **Auto-suggestions**: Get food name suggestions as you type with keyboard navigation
- **Responsive Design**: Works on desktop and mobile devices
- **Database Management**: Tools for managing the food database, including removing duplicates and cleaning data

## Project Structure

```
food_iq/
├── backend/
│   ├── models/
│   │   ├── Indian_Food_CNN_Model.h5
│   │   ├── database.py
│   │   ├── food.py
│   │   └── food_queries.py
│   ├── endpoints/
│   │   ├── food_router.py
│   │   ├── imageprocess.py
│   │   └── user_endpoint.py
│   ├── db/
│   │   ├── dbcreateandinsert.py
│   │   └── database.py
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Prerequisites

- Python 3.9+
- Node.js 20+ (via NVM recommended)
- PostgreSQL 15+
- Poetry (for Python dependency management)
- Docker and Docker Compose (optional)
- Make (for using the Makefile commands)
- TensorFlow 2.x
- SQLite (for development)

## Setup

### Environment Configuration

1. Create a `.env` file in the root directory:
   ```env
   DB_USERNAME=postgres
   DB_PASSWORD=postgres
   ```

2. Create a `.env` file in the backend directory:
   ```env
   # Database Configuration
   DATABASE_URL=sqlite:///./food_iq.db

   # Model Configuration
   MODEL_PATH=models/Indian_Food_CNN_Model.h5

   # Server Configuration
   PORT=8000
   HOST=0.0.0.0
   ```

### Database Setup

1. Initialize the database:
   ```bash
   make db-init
   ```

2. Remove duplicates (if needed):
   ```bash
   make db-remove-duplicates
   ```

### Model Setup

1. Place the TensorFlow model file (`Indian_Food_CNN_Model.h5`) in the `backend/models` directory

## Development

### Using Makefile

```bash
# Show all available commands
make help

# Install dependencies
make install

# Format code
make format
make format-backend
make format-frontend

# Run tests
make test
make test-coverage

# Database management
make db-init
make db-remove-duplicates
```

### Backend Development

```bash
# Install dependencies
cd backend
poetry install

# Run server
poetry run uvicorn main:app --reload

# Format code
poetry run black .

# Run tests
poetry run pytest
```

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev

# Format code
npx prettier --write "src/**/*.{js,jsx,ts,tsx,json,css,scss,md}"

# Check CSS syntax
npx stylelint "src/**/*.css"
```

### Database Management

```bash
# Initialize database
make db-init

# Remove duplicates
make db-remove-duplicates
```

## Deployment

### Docker Deployment

```bash
# Start all services
make docker-up

# Stop all services
make docker-down
```

### Local Deployment

#### Backend
```bash
cd backend
poetry install
poetry run uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Documentation

### Food Endpoints

- `GET /food/summary/{food_name}`: Get nutritional summary for a food item
- `GET /food/all`: Get all food items in the database

### Image Processing Endpoints

- `POST /image/predict`: Upload an image of food and get predictions with nutritional information
- `GET /image/food-classes`: Get a list of all food classes that can be recognized

## Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run backend tests
cd backend
poetry run pytest
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Pipeline Steps
1. Lint and Test
2. Build and Push Docker images

### Required Secrets
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` 