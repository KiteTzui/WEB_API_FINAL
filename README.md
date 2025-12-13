
# WEB_API_FINAL — Merge notes

What I changed
- Merged the simple FastAPI endpoints from `backend/main.py` into `fastapi_api/main.py` so the `fastapi_api` Docker service serves the API the frontend expects.

Why
- The `fastapi_api` service build context is `./fastapi_api` in `docker-compose.yml`. The `backend` app lived at `backend/main.py` and wasn't included in that build. Copying the API into `fastapi_api/main.py` makes the service runnable as-is.

Files changed
- `fastapi_api/main.py` — new merged FastAPI app (products endpoints + home route).

Current canonical API
- `fastapi_api/main.py` is the canonical API entrypoint used by `docker-compose`.
- The older `backend/main.py` is not used by `docker-compose` (it may be absent in this workspace). Do not delete `fastapi_api/main.py` unless you update compose and CI.

Run with Docker Compose
1) Build and start services:

```powershell
docker compose up --build
```

2) Services in the compose file:
- Django frontend: http://localhost:8000
- FastAPI API : http://localhost:8001 (endpoints: `/`, `/products`, `/products/{id}`)
- Postgres DB : port 5432

Quick local check (after compose up):

```powershell
curl http://localhost:8001/
curl http://localhost:8001/products
```

Notes and next steps
- I left `backend/main.py` intact as a reference — the running API is now `fastapi_api/main.py` used by the `fastapi_api` service.
- If you prefer to keep the API in `backend/`, we can change the `fastapi_api` build context to the repo root and update Dockerfiles accordingly.

