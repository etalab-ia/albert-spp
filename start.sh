#! /usr/bin/env bash

#PYTHONPATH=. alembic upgrade head
uvicorn app:app --host 0.0.0.0 --port 8090 --root-path /
