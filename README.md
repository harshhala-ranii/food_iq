# Food IQ - Indian Food Recognition and Recommendation System

A full-stack application for Indian food recognition and personalized food recommendations.

## Features

- Food image recognition using CNN
- Personalized food recommendations
- Health condition-based dietary guidance
- User profile management
- Food logging and tracking

## Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.8+ (for local backend development)
- OpenAI API key

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/food_iq.git
cd food_iq
```

2. Create environment files:
```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

3. Update the environment variables in `backend/.env`:
```
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_NAME=food_db
DB_PORT=5432
JWT_SECRET_KEY=your_jwt_secret_key
OPENAI_API_KEY=your_openai_api_key
PORT=8000
ENVIRONMENT=development
```

4. Update the environment variables in `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
```

## Running with Docker

1. Build and start the containers:
```bash
docker-compose up --build
```

2. The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Database: localhost:5432

## Development Setup

### Backend

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

## Security Notes

- Never commit `.env` files or sensitive credentials
- Keep your OpenAI API key secure
- Use strong passwords for database and JWT
- Regularly update dependencies for security patches

## License

MIT License 