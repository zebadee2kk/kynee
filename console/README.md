# KYNEE Console

The KYNEE console is a web-based command center that manages engagements, agents, findings, and audit logs.

**Important:** Use only with written authorization. See [ETHICAL_USE_POLICY.md](../ETHICAL_USE_POLICY.md).

---

## Requirements

- Docker 24+ (recommended)
- Docker Compose v2
- PostgreSQL 15+ (if running without Docker)
- Node.js 20+ (frontend development)
- Python 3.11+ (backend development)

---

## Quick Start (Docker)

A full docker-compose setup will be added in Week 5. Use this as a placeholder reference:

```bash
# From repo root
# docker compose up -d
```

---

## Configuration

Planned environment variables:

| Variable | Description | Example |
|---|---|---|
| `KYNEE_ENV` | Environment name | `dev` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://kynee:kynee@db:5432/kynee` |
| `JWT_SECRET` | JWT signing secret | `change-me` |
| `CONSOLE_BASE_URL` | Public URL for callbacks | `https://console.example.com` |
| `ALLOW_ORIGINS` | CORS origins | `https://console.example.com` |

---

## First Login (Planned)

1. Start the console services.
2. Create the first admin user (bootstrap command will be added).
3. Log in and create an engagement.

---

## Development

### Backend

```bash
cd console/backend
# Create venv, install requirements (to be added)
pytest tests/ -v
```

### Frontend

```bash
cd console/frontend
npm install
npm run dev
```

---

## Troubleshooting

**Database connection failed**
- Verify `DATABASE_URL` and network connectivity.

**CORS errors**
- Check `ALLOW_ORIGINS` and ensure correct protocol and port.

**JWT errors**
- Ensure `JWT_SECRET` is set and consistent across restarts.

---

## Status

The console is in **pre-alpha**. Expect breaking changes as Week 5 features land.
