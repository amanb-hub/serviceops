# ServiceOps — Architecture (Step 1: Foundation)

## Overview

ServiceOps is a multi-client vehicle/EV service ticket management platform. Step 1 establishes the foundation: project structure, database, authentication, and the application shell. No ticket workflows, dashboards, AI, or client-portal logic exist yet — those come in later steps.

## Request flow

```text
Frontend (Next.js / React)
      ↓  fetch("/api/...") with Authorization: Bearer <JWT>
FastAPI (app/main.py)
      ↓  routes in app/api/routes/*
Services (app/services/*)
      ↓  business logic, e.g. authenticate_user()
SQLAlchemy models (app/models/*)
      ↓  ORM layer
PostgreSQL
```

Future step: a **Claude AI layer** will sit alongside this stack to provide recommendations, classification, and summaries — but the application and database remain the single source of truth:

```text
User / Client
      ↓
ServiceOps Application
      ↓
Business Rules
      ↓
Database
      ↓
Claude AI (advisory only — never authoritative)
```

## Layers

- **Frontend (`frontend/`)** — Next.js App Router. `app/` holds routes, `components/` holds the shared shell (Sidebar, Topbar, AppShell, Card), `lib/` holds the API client and auth helpers, `hooks/` holds client-side data hooks. The frontend never trusts its own role checks for authorization — it reflects what the backend allows.

- **API layer (`backend/app/api/`)** — FastAPI routers. `deps.py` defines `get_current_user` (JWT validation) and `require_roles(...)` (RBAC). Every response follows `{ success, data, message }`.

- **Services (`backend/app/services/`)** — business logic separated from route handlers (e.g. `auth_service.authenticate_user`). Future ticket/SLA/inventory logic will follow the same pattern: routes stay thin, services hold the rules.

- **Models (`backend/app/models/`)** — SQLAlchemy ORM models mapping directly to the tables below. `mixins.py` provides `UUIDPKMixin` and `TimestampMixin` reused across models.

- **Database (PostgreSQL)** — see schema below. All IDs are UUIDs. Alembic manages schema changes (`backend/alembic/`).

## Database schema (Step 1)

```text
roles
  id, name, description, created_at

users
  id, name, email, phone, password_hash, role_id → roles.id,
  is_active, created_at, updated_at

clients
  id, name, code, contact_name, contact_email, contact_phone,
  status, created_at, updated_at

client_users   (join table: many users ↔ one client, one user can belong to multiple clients)
  id, client_id → clients.id, user_id → users.id, created_at
  unique(client_id, user_id)

cities
  id, name, state, country, status, created_at

audit_logs
  id, user_id → users.id (nullable), action, entity_type, entity_id,
  old_value, new_value, ip_address, created_at
```

Relationships:

```text
One client       → many client_users
One user          → one role
One role          → many permissions (future work)
Many clients      → completely isolated operational data
```

Every future operational table (vehicles, tickets, technicians, parts, reports) will carry a `client_id` foreign key so it can be scoped to the owning client. `clients`, `client_users`, and `cities` exist now precisely so those future tables have something to reference from day one.

## Authentication

- Passwords are hashed with bcrypt (`passlib`) — never stored in plain text.
- `POST /api/auth/login` verifies credentials and issues a JWT (`app/core/security.py`) containing the user id and role.
- `GET /api/auth/me` resolves the current user from the JWT via the `get_current_user` dependency.
- The frontend stores the JWT in `localStorage` and attaches it as a `Bearer` token on every API call (`frontend/lib/api.ts`).

## Multi-tenant security

`CLIENT_USER` accounts must only see data for the client(s) they are linked to via `client_users`. This is enforced **in the API layer**, not the frontend:

```python
# backend/app/api/routes/clients.py
if current_user.role.name in GLOBAL_CLIENT_ACCESS_ROLES:
    clients = db.query(Client).order_by(Client.name).all()
else:
    clients = (
        db.query(Client)
        .join(ClientUser, ClientUser.client_id == Client.id)
        .filter(ClientUser.user_id == current_user.id)
        .all()
    )
```

`SUPER_ADMIN` and `OPERATIONS_MANAGER` (and other internal-operations roles) can see all clients; `CLIENT_USER` cannot, regardless of what the frontend requests. This pattern — filter by role and client linkage inside the query, never trust a client-supplied filter alone — is the template every future operational endpoint (tickets, vehicles, parts, reports) should follow.

## Roles (RBAC foundation)

```text
SUPER_ADMIN
OPERATIONS_MANAGER
CITY_MANAGER
SERVICE_COORDINATOR
TECHNICIAN
CLIENT_USER
FINANCE_ADMIN
```

`app/api/deps.require_roles(*roles)` is a dependency factory used to gate individual endpoints (e.g. only `SUPER_ADMIN` / `OPERATIONS_MANAGER` may create clients or users). Fine-grained permissions per role are out of scope for Step 1 but the `roles` table and `role_id` foreign key are the anchor point for that future work.

## What's deliberately out of scope for Step 1

Ticket lifecycle, technician assignment, SLA engine, parts/inventory, client portal, AI integration, notifications (email/WhatsApp), advanced reports/analytics, mobile app, vehicle service history. These are listed in the README/spec and will be layered onto this foundation without restructuring it.
