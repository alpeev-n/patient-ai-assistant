# patient-ai-assistant

AI assistant for patients after receiving a medical diagnosis.

## What it does

- Provides psychological support: calms the patient and helps them understand and accept the diagnosis.
- Explains the diagnosis in plain, non‑technical language.
- Creates an actionable plan for next steps (e.g., follow‑up appointments, lifestyle changes).
- Generates a list of questions for the doctor.
- Recommends additional examinations (with explanations).

## Why it matters

Supporting patients emotionally and informationally right after a diagnosis can reduce anxiety, improve understanding, and lead to better adherence to treatment.

## Tech Stack

- Backend: Python 3.11+
- Framework: FastAPI
- AI provider: Groq API
- Database: PostgreSQL
- Message Queue: RabbitMQ
- Web Server: Nginx
- Containerization: Docker & Docker Compose

## Prerequisites

- Docker & Docker Compose (v2.0+)
- Or for local development: Python 3.11+, PostgreSQL 16, RabbitMQ

## Installation & Setup

### Using Docker Compose

1. **Clone the repository:**
```bash
git clone <repository-url>
cd patient-ai-assistant
```

2. **Create environment configuration:**
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=patient_ai
DATABASE_URL=postgresql://postgres:your_secure_password@database:5432/patient_ai

# Application
SECRET_KEY=your_secret_key_here
DEBUG=false

# AI Provider (Groq API)
GROQ_API_KEY=your_groq_api_key_here

# RabbitMQ
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
```

3. **Build and start all services:**
```bash
docker-compose up -d
```

This will start:
- **FastAPI backend** on http://localhost (via Nginx proxy)
- **PostgreSQL database** on port 5432
- **RabbitMQ** on port 5672 (management UI on port 15672)
- **ML Workers** (2 instances) for async prediction tasks

4. **Initialize the database:**
```bash
docker-compose exec app python -m app.init_db
```

5. **View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f database
```

6. **Stop services:**
```bash
docker-compose down
```

## Usage

### Web Interface

Access the web dashboard at:
- **http://localhost** (via Docker Compose)
- **http://localhost:8000** (local development)

**Features:**
- Register a new account
- Login to your account
- Submit medical information (diagnosis, examination results)
- View AI-generated structured response
- View prediction history

### API Endpoints

#### Authentication
- `POST /api/auth/register` — Create new user account
- `POST /api/auth/login` — Get JWT token
- `POST /api/auth/logout` — Invalidate token

#### Predictions
- `POST /api/predict` — Submit medical info and get AI analysis
- `GET /api/predict-history` — Get user's prediction history

#### Balance
- `GET /api/balance` — Check account balance
- `POST /api/balance/topup` — Add credits to account

#### Web Routes
- `GET /` — Dashboard (requires authentication)
- `GET /predict` — Prediction form
- `GET /history` — View prediction history

## Project Structure

```
app/
├── api/              # API route handlers
├── db/               # Database models
├── models/           # Domain models
├── schemas/          # Pydantic request/response schemas
├── services/         # Business logic services
├── web/              # Web interface routes
├── workers/          # ML worker processes
├── static/           # CSS, JavaScript files
├── templates/        # HTML templates
├── database.py       # Database connection
├── jwt.py            # JWT token handling
├── main.py           # FastAPI application
├── publisher.py      # RabbitMQ message publishing

docs/
└── design.md         # Domain model and architecture documentation

tests/
├── test_auth.py      # Authentication tests
├── test_predict.py   # Prediction API tests
├── test_db.py        # Database tests
└── ...

docker-compose.yml   # Service orchestration
Dockerfile           # App container
web-proxy/           # Nginx configuration
worker/              # ML worker container
```
