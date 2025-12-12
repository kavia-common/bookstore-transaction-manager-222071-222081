"""
PUBLIC_INTERFACE
Regenerate the OpenAPI spec (interfaces/openapi.json) from the FastAPI application.

Usage:
    python -m scripts.regen_openapi
"""
import json
import os

from src.api.main import app  # ensure app is imported after all routers and overrides

def main() -> None:
    schema = app.openapi()
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "interfaces")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "openapi.json")
    with open(out_path, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"Wrote OpenAPI schema to {out_path}")

if __name__ == "__main__":
    main()
