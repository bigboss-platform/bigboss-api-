# BigBoss API — Claude Context

## Current Task
Check `docs/fastfood/tasks/INDEX.md` in the `bigboss` repo for current task status.  
Task files live at `docs/fastfood/tasks/TASK-XX-[STATUS]-name.md`.

## What This Is
FastAPI modular monolith backend for the BigBoss SaaS platform.  
Currently serving the FastFood vertical (tenant-aware, multi-tenant via PostgreSQL schemas).

## Stack
- Python 3.12, FastAPI 0.115, SQLAlchemy 2.x async, Pydantic v2, Alembic, asyncpg
- PostgreSQL 16, Redis 7, Celery (future)
- Dev environment: Dev Container only — never run anything locally outside Docker

## Project Structure
```
app/
  core/         — config, database, middleware, security, dependencies, exceptions
  modules/      — feature modules (auth, tenants, end_users, menus, orders, tenant_admins)
  shared/       — base classes, enums, utils used across modules
migrations/     — Alembic env + versions
tests/
  unit/         — no DB, mock everything external
  integration/  — real test DB, real HTTP calls
  contract/     — schemathesis API contract tests
scripts/        — seed.py and other one-off scripts
```

## Module Structure (every module has these files)
```
models.py       — SQLAlchemy ORM models
schemas.py      — Pydantic request/response schemas
repository.py   — DB queries only, no business logic
service.py      — business logic, calls repository
router.py       — FastAPI routes, calls service
public.py       — THE ONLY FILE other modules may import from
exceptions.py   — module-specific exceptions
dependencies.py — FastAPI Depends() factories for this module
```

## Hard Rules — Never Break These

### SQLAlchemy
- Always use `select()` + `await session.execute()` — never `.query()`
- Always `await session.commit()` after writes — handled in `get_db_session()` generator
- Eager load relationships with `selectinload()` to avoid N+1
- UUID primary keys always, stored as `UUID(as_uuid=True)`

### Data
- Never hard delete — always `is_deleted = True` (soft delete)
- `TimestampedBase` for all tenant-schema models, `Base` for public-schema models
- Tenant data lives in `tenant_{id}` schema — switch via `set_tenant_schema()` in `database.py`
- Public data (tenants, tenant_admins, themes, settings) lives in `public` schema

### Errors
- All business errors must subclass `BigBossException` from `app/shared/exceptions.py`
- Never raise plain `HTTPException` — use the typed exception subclasses
- All errors return RFC 7807 JSON: `type`, `title`, `status`, `detail`, `instance`

### Module Boundaries
- Other modules import ONLY from `module/public.py` — never from internals
- A module's `service.py` may call another module's service via its `public.py`
- `router.py` never imports from another module's internals

### Pydantic
- Always `model_validate()` — never `parse_obj()`
- Use `ConfigDict(from_attributes=True)` on read schemas
- Field validators use `@field_validator`

### Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- DB columns: `snake_case`
- Pydantic schemas: suffix `Schema` (e.g. `OrderCreateSchema`, `OrderReadSchema`)

## Terminology — Strictly Enforced
- `Tenant` — the business that uses BigBoss (never "customer", "client", "store")
- `End User` — the person placing orders via the FastFood app (never "customer" alone)
- `Tenant Admin` — staff member with back office access

## Auth
- End Users authenticate via OTP (phone → 6-digit code)
- Tenant Admins authenticate via email + password
- JWT access token (15 min) + refresh token (7 days)
- `require_end_user()`, `require_tenant_admin()`, `require_platform_admin()` are the FastAPI dependencies

## Running Things (inside Dev Container)
```bash
alembic upgrade head          # run migrations
python scripts/seed.py        # seed demo data
uvicorn app.main:app --reload # start API on :8000
pytest tests/unit -v          # unit tests
pytest tests/integration -v   # integration tests
```

## Forbidden Patterns
- `session.query()` — use `select()`
- Importing from `module/service.py` or `module/models.py` from outside the module
- Hard deletes (`session.delete()`) — use soft delete
- `null` / `None` as a business value — use typed optionals only at boundaries
- Plain `raise HTTPException` — use typed exceptions
- `.parse_obj()` — use `.model_validate()`
