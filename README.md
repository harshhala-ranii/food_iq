# Food IQ Application

A web application for retrieving nutritional information about food items and identifying Indian food from images.

## Project Structure

- **Backend**: FastAPI application with PostgreSQL database
- **Frontend**: React application with Material UI

## Features

- **Food Nutritional Information**: Get detailed nutritional information about various food items
- **Food Image Recognition**: Upload images of Indian food and get predictions with nutritional information
- **Database Management**: Tools for managing the food database, including removing duplicates and cleaning data

## Local Development

### Prerequisites

- Python 3.9+
- Node.js 20+ (via NVM recommended)
- PostgreSQL 15+
- Poetry (for Python dependency management and formatting)
- Docker and Docker Compose (optional)
- Make (for using the Makefile commands)

### Setup

1. Clone the repository
2. Create a `.env` file in the root directory with the following variables:
   ```
   DB_USERNAME=postgres
   DB_PASSWORD=postgres
   ```
3. Place the TensorFlow model file (`Indian_Food_CNN_Model.h5`) in the `backend/models` directory

### Using the Makefile

This project includes a Makefile that provides convenient commands for common development tasks. **Always run these commands with the `make` prefix**:

```bash
# Show all available commands
make help

# Install all dependencies
make install

# Initialize the database
make db-init

# Remove duplicate records from the database
make db-remove-duplicates

# Run linting
make lint

# Format code
make format                # Format both backend and frontend
make format-backend        # Format only backend code with Black
make format-frontend       # Format only frontend code with Prettier

# Check CSS syntax
make check-css             # Check and fix CSS syntax errors

# Run tests
make test

# Run tests with coverage
make test-coverage

# Start all services with Docker Compose
make docker-up

# Stop all services
make docker-down
```

#### Node.js Version Management

The Makefile uses NVM (Node Version Manager) to ensure the correct Node.js version is used. By default, it uses Node.js 20. You can specify a different version:

```bash
# Use a specific Node.js version
make lint-frontend NODE_VERSION=16
make install-frontend NODE_VERSION=18
```

Make sure NVM is installed and properly set up in your environment. The Makefile will automatically run `nvm use` before executing npm commands.

### Poetry for Backend Development

The backend uses Poetry for dependency management and code formatting:

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies with Poetry
cd backend
poetry install

# Format code with Black
poetry run black .

# Run tests with Poetry
poetry run pytest
```

You can also use the Makefile command `make format-backend` which will check if Poetry is installed, install it if needed, and run Black on the backend code.

### Prettier and Stylelint for Frontend Development

The frontend uses Prettier for code formatting and Stylelint for CSS syntax checking:

```bash
# Install dependencies
cd frontend
npm install

# Format code with Prettier
npx prettier --write "src/**/*.{js,jsx,ts,tsx,json,css,scss,md}"

# Check formatting without changing files
npx prettier --check "src/**/*.{js,jsx,ts,tsx,json,css,scss,md}"

# Check CSS syntax with Stylelint
npx stylelint "src/**/*.css"

# Fix CSS syntax issues automatically
npx stylelint "src/**/*.css" --fix
```

You can also use the Makefile commands:
- `make format-frontend` - Formats frontend code with Prettier (runs CSS syntax check first)
- `make check-css` - Checks and fixes CSS syntax errors with Stylelint

### Database Management

The project includes several commands for managing the PostgreSQL database:

```bash
# Initialize the database with sample data
make db-init

# Remove duplicate records from the database
make db-remove-duplicates
```

The duplicate removal script (`backend/remove_duplicates.py`) provides three methods:
1. `remove_duplicates()` - Removes duplicates based on all nutritional values
2. `remove_duplicates_alternative()` - Alternative method using SQLAlchemy ORM
3. `remove_duplicates_by_food_product()` - Removes duplicates keeping only one record per food product

You can edit the script to choose which method to use based on your needs.

### Running with Docker Compose

```bash
# Using Makefile
make docker-up

# Or directly with Docker Compose
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Backend API on port 8000
- Frontend application on port 80

### Running Locally

#### Backend

```bash
# Using Makefile
make install-backend
make db-init
cd backend && uvicorn main:app --reload

# Or using Poetry
cd backend
poetry install
poetry run python dbcreateandinsert.py
poetry run uvicorn main:app --reload
```

#### Frontend

```bash
# Using Makefile
make install-frontend
make frontend-dev

# Or manually
cd frontend
nvm use 20  # Make sure to use the correct Node.js version
npm install
npm run dev
```

## API Endpoints

### Food Endpoints

- `GET /food/summary/{food_name}`: Get nutritional summary for a food item
- `GET /food/all`: Get all food items in the database

### Image Processing Endpoints

- `POST /image/predict`: Upload an image of food and get predictions with nutritional information
- `GET /image/food-classes`: Get a list of all food classes that can be recognized

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

### Pipeline Steps

1. **Lint and Test**:
   - Formats Python code with Black
   - Formats JavaScript/TypeScript code with Prettier
   - Checks CSS syntax with Stylelint
   - Lints Python code with flake8
   - Lints JavaScript/TypeScript code with ESLint
   - Runs Python tests with pytest
   - Uploads test coverage to Codecov

2. **Build and Push**:
   - Builds Docker images for backend and frontend
   - Pushes images to Docker Hub

### Setting Up the Pipeline

1. Add the following secrets to your GitHub repository:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token

2. Push to the main/master branch to trigger the pipeline

### Running Tests Locally

```bash
# Using Makefile
make test
make test-coverage

# Or using Poetry
cd backend
poetry run pytest
poetry run pytest --cov=. --cov-report=term
``` 