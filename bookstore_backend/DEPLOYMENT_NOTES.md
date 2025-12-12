# Bookstore Backend - Deployment Notes

- CORS
  - Configure allowed origins via environment variable: `ALLOW_ORIGINS`
  - For development: `ALLOW_ORIGINS="*"`
  - For preview/staging, set to specific origins: 
    e.g. `ALLOW_ORIGINS="https://preview.example.com,https://staging.example.com"`

- Security
  - Set a strong `SECRET_KEY`
  - Optionally adjust `ACCESS_TOKEN_EXPIRE_MINUTES` and `JWT_ALGORITHM`

- Database
  - Default uses SQLite: `DATABASE_URL=sqlite:///./bookstore.db`
  - For Postgres: `DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME`
    - Ensure the driver is available in the environment

- Dependencies
  - Required for auth and ORM:
    - SQLAlchemy
    - passlib[bcrypt]
    - python-jose[cryptography]

- Auth flow
  - Register: POST /auth/register
  - Login: POST /auth/login -> returns `{ "access_token": "…", "token_type": "bearer" }`
  - Use `Authorization: Bearer <token>` for protected routes.
