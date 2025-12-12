# bookstore-transaction-manager-222071-222081

Backend (FastAPI) integration notes

- Entry point: bookstore_backend/src/api/main.py
- Run locally: make -C bookstore_backend run (serves at http://localhost:3001)
- API docs: http://localhost:3001/docs
- Regenerate OpenAPI file: make -C bookstore_backend regen-openapi (writes to bookstore_backend/interfaces/openapi.json)

Auth flow
- Register: POST /auth/register
- Login: POST /auth/login -> returns access_token and token_type
- Use header Authorization: Bearer <access_token> for protected endpoints

Transactions CRUD
- GET /transactions?skip=0&limit=50
- POST /transactions
- PUT /transactions/{id}
- DELETE /transactions/{id}
- GET /transactions/summary

CORS
- Configure allowed origins via env var ALLOW_ORIGINS (comma-separated). Use "*" during development.
- See bookstore_backend/.env.example for reference.

Environment
- See bookstore_backend/ENVIRONMENT_VARIABLES.md for required variables.