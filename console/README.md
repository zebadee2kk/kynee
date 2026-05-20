# KYNEĒ Console

The KYNEĒ console is a web-based command center for managing security assessments. It provides:
- **Engagement management**: Define scope, Rules of Engagement, authorized methods
- **Agent management**: Enroll agents, monitor status, dispatch jobs
- **Findings dashboard**: Review and triage discoveries, track remediation
- **Audit logs**: Immutable compliance records, forensic analysis

**Important:** Use only with written authorization. See [../ETHICAL_USE_POLICY.md](../ETHICAL_USE_POLICY.md).

**Status**: Pre-Alpha (Week 1-2 scaffolding complete, Week 3-5 implementation in progress)

---

## 📋 Architecture

The console is split into two main parts:

### Backend (FastAPI)
- RESTful API for agents, engagements, findings
- Authentication & authorization (JWT)
- Database layer (SQLAlchemy ORM)
- Audit log persistence
- WebSocket support for real-time updates

### Frontend (React + TypeScript)
- Dashboard for system overview
- Agent management UI
- Findings browser and triage interface
- Engagement configuration
- Real-time status monitoring

---

## 🛠️ Developer Setup

### Backend

```bash
cd console/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Start development server
python -m kynee_console_backend.main
# API available at http://localhost:8000
# Docs at http://localhost:8000/api/docs
```

### Frontend

```bash
cd console/frontend

# Install dependencies
npm install

# Start development server (with hot reload)
npm run dev
# Available at http://localhost:5173
# Proxies API calls to http://localhost:8000

# Lint and format
npm run lint
npm run format

# Type checking
npm run type-check

# Build for production
npm run build
```

### Project Structure (Backend)

```
console/backend/
├── pyproject.toml
├── kynee_console_backend/
│   ├── __init__.py
│   ├── main.py                # Entry point
│   ├── app/
│   │   └── __init__.py        # FastAPI app factory
│   ├── routers/               # API endpoint handlers
│   │   ├── agents.py          # /api/v1/agents/*
│   │   ├── findings.py        # /api/v1/findings/*
│   │   └── engagements.py     # /api/v1/engagements/*
│   ├── schemas/               # Pydantic request/response models
│   │   ├── agent.py
│   │   ├── finding.py
│   │   └── engagement.py
│   ├── models/                # SQLAlchemy database models
│   │   └── __init__.py
│   ├── db/                    # Database connection & migrations
│   │   └── __init__.py
│   └── core/                  # Config, auth, utilities
│       └── __init__.py
└── tests/
    ├── test_app.py
    └── test_routers.py        # (to be added)
```

### Project Structure (Frontend)

```
console/frontend/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── src/
│   ├── main.tsx               # Entry point
│   ├── App.tsx                # Root component with routing
│   ├── types/
│   │   └── index.ts           # TypeScript type definitions
│   ├── services/
│   │   └── api.ts             # Axios API client
│   ├── components/            # Reusable React components
│   ├── pages/                 # Page components (dashboard, agents, etc.)
│   ├── hooks/                 # Custom React hooks
│   └── styles/
│       ├── App.css
│       └── index.css
└── tests/                     # (to be added)
```

---

## 🚀 Quick Start (Local Development)

Start both backend and frontend:

```bash
# Terminal 1: Backend
cd console/backend
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
python -m kynee_console_backend.main

# Terminal 2: Frontend
cd console/frontend
npm install
npm run dev

# Open http://localhost:5173 in browser
```

---

## 🗄️ Database (Coming Week 4)

SQLAlchemy models and migrations will be added in Week 4:

```bash
# Run migrations
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "Add findings table"
```

Environment variables:
```bash
DATABASE_URL=<set-db-url-in-env>
SQLALCHEMY_ECHO=true  # Log SQL queries
```

---

## 🔐 Authentication (Coming Week 5)

JWT-based authentication will be implemented:

```python
# Backend
from kynee_console_backend.core.security import create_access_token

jwt = create_access_token(data={"sub": "user_id"})
```

```typescript
// Frontend
const response = await api.post('/auth/login', {
  username: 'admin',
  password: 'password'
});
localStorage.setItem('access_token', response.data.access_token);
```

---

## 📝 Testing

```bash
# Backend unit tests
cd console/backend
pytest tests/ -v --cov=kynee_console_backend

# Frontend unit tests
cd console/frontend
npm test

# E2E tests (coming later)
# npm run test:e2e
```

---

## 🐳 Docker Deployment (Week 5)

Coming soon: docker-compose setup with:
- FastAPI backend
- PostgreSQL database
- React frontend (nginx)
- nginx reverse proxy
- WireGuard VPN gateway

---

## 🔗 API Documentation

Auto-generated OpenAPI docs available at:
```
http://localhost:8000/api/docs          # Swagger UI
http://localhost:8000/api/redoc         # ReDoc
```

### Current Endpoints (Stubs)

```
GET    /health                           # Health check
GET    /api/v1/agents                    # List agents
POST   /api/v1/agents/enroll             # Enroll new agent
GET    /api/v1/findings                  # List findings
POST   /api/v1/findings                  # Create finding
GET    /api/v1/engagements               # List engagements
```

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|---|---|---|
| `KYNEE_ENV` | Environment (dev/prod) | `dev` |
| `DATABASE_URL` | PostgreSQL connection | `sqlite:///kynee.db` |
| `JWT_SECRET` | JWT signing key | `change-me` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:5173` |
| `LOG_LEVEL` | Log level | `info` |

---

## 🤝 Contributing

1. Backend: `feat/console-backend-<feature>`
2. Frontend: `feat/console-frontend-<feature>`
3. Follow [../docs/ops/branching-and-ai-collaboration.md](../docs/ops/branching-and-ai-collaboration.md)

---

## 📚 References

- [ADR-0002: Transport Design](../docs/architecture/adr-0002-transport.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React + TypeScript Guide](https://react-typescript-cheatsheet.netlify.app)
- [Pydantic Documentation](https://docs.pydantic.dev)
