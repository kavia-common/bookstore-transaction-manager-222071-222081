# Required environment variables

These variables should be provided via the environment (e.g., .env). Do not commit secrets.

- SECRET_KEY: Strong random string used to sign JWTs.
- ACCESS_TOKEN_EXPIRE_MINUTES: Integer minutes for token expiry (default 60).
- JWT_ALGORITHM: JWT signing algorithm (default HS256).
- DATABASE_URL: SQLAlchemy URL. Default: sqlite:///./bookstore.db
- ALLOW_ORIGINS: Comma-separated list of allowed CORS origins. Use "*" for development.

Example (.env):
SECRET_KEY=CHANGE_ME_DEV_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_ALGORITHM=HS256
DATABASE_URL=sqlite:///./bookstore.db
ALLOW_ORIGINS=*
