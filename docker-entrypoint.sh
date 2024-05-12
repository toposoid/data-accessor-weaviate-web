#!/bin/bash

cd /app/data-accessor-weaviate-web
uvicorn api:app --reload --host 0.0.0.0 --port $$TOPOSOID_DATA_ACCESSOR_PORT
