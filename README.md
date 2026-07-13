# Trace - Dashboard for Self-Hosted Servers

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Trace** is a unified dashboard for enthusiasts deploying home servers. It solves the problem of lacking a convenient, visually uncluttered tool for monitoring home infrastructure.

## Key Features

- Server (Agent) Management: registration, status monitoring, deletion.
- Status Monitoring: tracking agent statuses via Heartbeat mechanism.
- Logging: view and stream logs (including tail -f via WebSocket).
- Security: JWT authentication with refresh tokens, endpoint protection.
- Database: PostgreSQL (primary) and SQLite (for development/testing).

## Technology Stack

- Backend: Python 3.11+, FastAPI, Uvicorn
- Database: PostgreSQL (asyncpg), SQLite (aiosqlite), SQLAlchemy 2.0, Alembic
- Authentication: JWT (python-jose), bcrypt
- Logs and Files: aiofiles
- Testing: pytest, pytest-asyncio
- Dependency Management: Poetry / pip

## Quick Start

### Requirements

- Python 3.11 or higher
- PostgreSQL (for production) or SQLite (for development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/flinteus/Trace.git
   cd Trace
   ```

2. Install dependencies via Poetry (recommended):
   ```bash
   poetry install
   ```
   Or via pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file in the project root:
   ```env
   # JWT
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7

   # Database
   DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/trace_db

   # App
   APP_NAME=Trace
   DEBUG=True
   ```

4. Apply migrations:
   ```bash
   poetry run alembic upgrade head
   ```

5. Start the server:
   ```bash
   poetry run uvicorn main:app --reload
   ```

6. Open Swagger documentation:
   [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /login   | User login (JWT access + refresh) |
| POST   | /refresh | Refresh access token |
| POST   | /logout  | Logout (token invalidation) |
| POST   | /registration | New user registration |

### Agent Management (`/api/v1/agents`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /register | Register a new server (agent) |
| GET    | /         | Get list of user's agents |
| GET    | /{agent_id} | Get specific agent details |
| PUT    | /{agent_id} | Update agent data |
| DELETE | /{agent_id} | Delete an agent |
| POST   | /heartbeat | Update agent status (auto-registration) |

### Logs (`/api/v1/logs`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /agents/{agent_id}/logs | List available log files |
| GET    | /agents/{agent_id}/logs/{log_name} | Read log content |
| WebSocket | /ws/agents/{agent_id}/logs/{log_name} | Real-time log streaming |

## Testing

Run all tests:
```bash
poetry run pytest -v
```

Run with coverage:
```bash
poetry run pytest --cov=app --cov-report=html
```

## Project Structure

```
Trace/
├── app/
│   ├── api/             # Endpoints (FastAPI routers)
│   ├── core/            # Configuration, DB, dependencies
│   ├── models/          # SQLAlchemy models
│   ├── repository/      # Data access layer
│   ├── schemas/         # Pydantic schemas (validation)
│   └── services/        # Business logic
├── migrations/          # Alembic migrations
├── tests/               # Tests
├── main.py              # Entry point
├── pyproject.toml       # Dependencies (Poetry)
├── requirements.txt     # Dependencies (pip)
└── README.md
```

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/amazing-feature`.
3. Commit your changes: `git commit -m 'Add some amazing feature'`.
4. Push to the branch: `git push origin feature/amazing-feature`.
5. Open a Pull Request.

## Development Roadmap

- [ ] Go agent for collecting metrics (CPU, RAM, Disk)
- [ ] Alerting and notification system
- [ ] Web interface for real-time metrics
- [ ] Remote service management (start/stop)
- [ ] Integration with DDNS services (ddns-go)

## License

Distributed under the MIT License. See `LICENSE` file for details.

---

Made for Homelab enthusiasts
