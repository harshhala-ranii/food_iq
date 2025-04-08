# Food IQ Backend

A FastAPI backend for the Food IQ application that provides personalized food recommendations based on user profiles and image recognition.

## Docker Setup

The backend is containerized using Docker for easy deployment and consistent execution across environments.

### Prerequisites

1. Docker and Docker Compose installed on your system
2. PostgreSQL (installed or as a Docker container)

### Docker Configuration

1. Create a `.env` file in the `backend/` directory (copy from `.env.example`):

```bash
cp .env.example .env
```

2. Edit the `.env` file to set the database credentials and other environment variables:

```
# Database configuration
DB_USERNAME=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=db  # Use 'db' as hostname when using the PostgreSQL container
DB_PORT=5432
DB_NAME=foodiq
```

### Building and Running with Docker

Build and start the Docker containers:

```bash
docker-compose up --build
```

This will start both the backend API service and the PostgreSQL database.

To run in detached mode:

```bash
docker-compose up -d
```

To stop the containers:

```bash
docker-compose down
```

## Manual Setup (Without Docker)

If you prefer to run the application without Docker:

### Database Setup

1. Install PostgreSQL and create a database:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create a new database
CREATE DATABASE foodiq;

# Exit PostgreSQL
\q
```

2. Install required Python packages:

```bash
pip install -r requirements.txt
```

3. Initialize the database:

```bash
python init_db.py --reset  # Reset and recreate all tables
python init_db.py --test-data  # Add test data
```

4. Run the application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

The Food IQ API provides the following main endpoints:

### Authentication

- `POST /auth/register`: Register a new user
- `POST /auth/register-with-profile`: Register a new user with profile information
- `POST /auth/token`: Login to get an access token
- `GET /auth/users/me`: Get current user information
- `GET /auth/users/me/profile`: Get current user's profile
- `POST /auth/users/me/profile`: Create user profile
- `PUT /auth/users/me/profile`: Update user profile

### User Management

- `GET /users/me`: Get current user data
- `GET /users/me/profile`: Get current user profile
- `GET /users/me/food-logs`: Get food logs for the current user
- `POST /users/me/food-logs`: Add a food item to user's food log
- `GET /users/me/recommendations`: Get food recommendations for the current user
- `DELETE /users/me`: Delete current user account

### Image Processing

- `POST /image/predict`: Predict food from an uploaded image
- `POST /image/predict-with-recommendation`: Predict food and generate recommendations
- `POST /image/analyze`: Comprehensive food analysis with macronutrient breakdown
- `GET /image/food-classes`: Get all available food classes that the model can predict

## Authentication Flow

The API uses JWT (JSON Web Tokens) for authentication:

1. Register a user with `POST /auth/register` or `POST /auth/register-with-profile`
2. Login with `POST /auth/token` to get an access token
3. Use the access token in the Authorization header for protected endpoints: `Authorization: Bearer {token}`

## Database Models

The database includes the following main models:

- `User`: Stores user authentication information
- `UserProfile`: Stores user profile information including health details
- `Food`: Stores food nutritional information
- `UserFoodLog`: Tracks user food consumption
- `FoodRecommendation`: Stores personalized food recommendations

### Database Schema

The database schema has the following tables and relationships:

- `users`: Main user table with authentication data
  - Has one-to-one relationship with `user_profiles`
  - Has one-to-many relationship with `user_food_logs`
  - Has one-to-many relationship with `food_recommendations`

- `user_profiles`: Extended user information including health data
  - Belongs to one user in `users`

- `food`: Food items with nutritional information
  - Referenced by `user_food_logs`

- `user_food_logs`: Records of food consumed by users
  - Belongs to one user in `users`
  - References one food item in `food`

- `food_recommendations`: Personalized food recommendations
  - Belongs to one user in `users`
  - Can reference multiple food items through the `food_ids` column

## Development

### Adding New Models

To add a new model to the database:

1. Define the model class in the appropriate file in the `models/` directory
2. Import the model in `main.py`
3. Rebuild and restart the Docker containers to apply changes

#### Model Definition Guidelines

When adding new models, follow these guidelines to avoid conflicts:

- Ensure each model has a unique `__tablename__` value
- Never define the same model class in multiple files
- Use appropriate relationships and foreign keys
- When in doubt, check existing model definitions to avoid duplications

### Adding New Endpoints

To add a new endpoint:

1. Create a new file in the `endpoints/` directory or add to an existing one
2. Define the router and endpoints using FastAPI
3. Import and include the router in `main.py`

## Troubleshooting

- **Database Connection Issues**: Ensure PostgreSQL is running and the credentials in `.env` are correct
- **Import Errors**: Check the Docker image has all required dependencies (specified in requirements.txt)
- **Model Loading Errors**: Ensure the TensorFlow model file exists at the specified path
- **Database Model Conflicts**: Check model definitions for duplications, particularly across different files
- **SQLAlchemy Errors**: Check your model definitions for inconsistencies, especially foreign key references
- **Docker Issues**: Check logs with `docker-compose logs` and ensure ports are not in use by other services 