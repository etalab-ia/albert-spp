#! /usr/bin/env bash

#PYTHONPATH=. alembic upgrade head
uvicorn appn:app --host 0.0.0.0 --port 8090 --root-path /
