# Convenience targets for local development

.PHONY: run regen-openapi

run:
\tuvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

regen-openapi:
\tpython -m scripts.regen_openapi
