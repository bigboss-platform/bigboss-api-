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

## Codebase Gotchas — Read Before Touching These Areas

**Exception subclasses:** `BigBossException` sets `status_code`, `error_type`, `title`, `detail` as **class attributes** — not `__init__` kwargs. Subclasses define them at class level and call `super().__init__()` with no args (or omit `__init__` entirely).

**Model IDs are always `String`:** Every primary key and every FK is `Mapped[str] = mapped_column(String, ...)`. Never use `UUID(as_uuid=True)` — that was a bug that was fixed. String UUIDs via `uuid4()` everywhere.

**Cross-module slug resolution:** When a router receives a `tenant_slug` from the URL path and needs to call a service from a different module, it must resolve the slug to a `tenant_id` first via `TenantService.resolve_tenant_id()`. Import `TenantService` and `get_tenant_service` from `app.modules.tenants.public` — never from internals. See `menus/router.py` for the established pattern.

**`public.py` exports dependency factories:** When another module needs a service as a FastAPI dependency, the factory function (`get_X_service`) must be exported from `module/public.py`. This is how cross-module dependency injection stays boundary-clean.

## Forbidden Patterns
- `session.query()` — use `select()`
- Importing from `module/service.py` or `module/models.py` from outside the module
- Hard deletes (`session.delete()`) — use soft delete
- `null` / `None` as a business value — use typed optionals only at boundaries
- Plain `raise HTTPException` — use typed exceptions
- `.parse_obj()` — use `.model_validate()`
