# ServiceOps

**Multi-Client Service Management Platform**

ServiceOps is a service-ticket management platform built for an operations company that manages vehicle/EV service work on behalf of multiple clients (e.g. Delhivery, Porter, Zomato, Flipkart, Blue Dart, Express Bees, and future clients). It is designed from the ground up to be **configurable and multi-tenant** — no client is hard-coded into the application.

This repository currently contains **Step 1: Project Foundation** — architecture, database, authentication, and the application shell. Ticket workflows, dashboards, inventory, AI features, and client portals will be built in later steps.

---

## 1. Technology Stack

**Frontend:** Next.js (App Router), React, TypeScript, Tailwind CSS, shadcn-style components, Lucide icons

**Backend:** Python, FastAPI, Pydantic, SQLAlchemy, Alembic

**Database:** PostgreSQL

**Auth:** JWT + bcrypt password hashing, role-based access control (RBAC) foundation

**Infra:** Docker, Docker Compose, `.env`-based configuration

---

## 2. Folder Structure

```text
serviceops/
├── frontend/            Next.js app (App Router)
│   ├── app/              routes: /login, /dashboard, /clients, ...
│   ├── components/       Sidebar, Topbar, AppShell, Card, etc.
│   ├── lib/               api.ts, auth.ts, utils.ts
│   ├── hooks/             use-current-user.ts
│   ├── types/             shared TS types
│   └── styles/            Tailwind globals
├── backend/              FastAPI app
│   ├── app/
│   │   ├── api/           routes + auth dependency (RBAC)
│   │   ├── core/          config, security (JWT/bcrypt)
│   │   ├── db/             session, seed script
│   │   ├── models/         SQLAlchemy models
│   │   ├── schemas/        Pydantic schemas
│   │   └── services/       business logic (auth_service, ...)
│   ├── alembic/            migrations
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
└── docs/
    └── architecture.md
```

---

## 3. Configure `.env`

Copy the example file and fill in real values:

```bash
cp .env.example .env
```

Set at minimum:

- `JWT_SECRET` — a long random string
- `SEED_ADMIN_PASSWORD` — the password for the first admin account (never commit this)

---

## 4. Start PostgreSQL

Via Docker Compose (recommended — see §5 for the full stack), or standalone:

```bash
docker compose up -d postgres
```

---

## 5. Start Everything with Docker Compose

```bash
docker compose up --build
```

This starts:

- `postgres` on `localhost:5432`
- `backend` (FastAPI) on `localhost:8000`
- `frontend` (Next.js) on `localhost:3000`

---

## 6. Run Backend Standalone (without Docker)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export $(cat ../.env | xargs)   # or use a tool like direnv
uvicorn app.main:app --reload
```

---

## 7. Run Frontend Standalone (without Docker)

```bash
cd frontend
npm install
npm run dev
```

---

## 8. Run Migrations

With the backend's virtualenv active and `DATABASE_URL` pointing at a running Postgres:

```bash
cd backend
alembic upgrade head
```

---

## 9. Create the First Admin User

The admin is created by the seed script, **not** hard-coded. Set `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD` in `.env`, then:

```bash
cd backend
python -m app.db.seed
```

This creates:
- The 7 canonical roles (`SUPER_ADMIN`, `OPERATIONS_MANAGER`, `CITY_MANAGER`, `SERVICE_COORDINATOR`, `TECHNICIAN`, `CLIENT_USER`, `FINANCE_ADMIN`)
- One `SUPER_ADMIN` user using the credentials from `.env`
- Sample clients (Delhivery, Porter, Zomato, Flipkart) and cities (Gurgaon, Delhi, Bangalore, Mumbai, Hyderabad, Pune) — development seed data only

---

## 10. Using the App

1. Open `http://localhost:3000` → redirects to `/login`
2. Sign in with the seeded admin credentials
3. You'll land on `/dashboard` with placeholder KPI cards
4. Visit `/clients` to see the client list and create a new client
5. All other sidebar modules show "Module coming in the next development phase"

---

## Notes

- No client (e.g. "Delhivery") is hard-coded anywhere in the application — clients are data.
- Multi-tenant data isolation is enforced **server-side** in the API layer, not just the frontend (see `backend/app/api/routes/clients.py`).
- Claude/AI integration is intentionally not part of this step — see `docs/architecture.md` for where it will sit in the stack.
