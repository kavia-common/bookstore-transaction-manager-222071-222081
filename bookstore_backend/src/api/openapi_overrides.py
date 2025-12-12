from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def apply_openapi_overrides(app: FastAPI) -> None:
    """
    PUBLIC_INTERFACE
    Apply OpenAPI customizations such as explicit security schemes.

    This ensures the OAuth2 password flow appears clearly in the generated
    OpenAPI spec (useful for frontend clients and SDK generators).
    """
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            tags=app.openapi_tags,
        )
        # Define security scheme for OAuth2 password flow
        openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})
        openapi_schema["components"]["securitySchemes"]["OAuth2PasswordBearer"] = {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {},
                }
            },
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore[attr-defined]
