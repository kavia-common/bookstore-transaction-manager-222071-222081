from fastapi import APIRouter

router = APIRouter(tags=["health"], include_in_schema=False)

# PUBLIC_INTERFACE
@router.get("/api-usage")
def api_usage():
    """Developer help endpoint describing how to authenticate and call protected routes."""
    return {
        "auth": {
            "register": {"method": "POST", "path": "/auth/register"},
            "login": {"method": "POST", "path": "/auth/login", "returns": ["access_token", "token_type"]},
            "header": "Authorization: Bearer <access_token>",
        },
        "protected_routes": ["/transactions", "/transactions/summary", "/transactions/{id}"],
        "notes": [
            "Include the Bearer token from /auth/login in the Authorization header for all protected endpoints.",
            "Ensure the frontend origin is allowed by backend CORS via ALLOW_ORIGINS env (comma-separated).",
        ],
    }
