#!/bin/bash

cd /app/data-accessor-weaviate-web
source /root/.local/bin/env
uv run uvicorn api:app --reload --host 0.0.0.0 --port ${TOPOSOID_DATA_ACCESSOR_PORT}
